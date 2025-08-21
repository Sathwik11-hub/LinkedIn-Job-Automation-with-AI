"""
Vector store utility for RAG embeddings and similarity search
"""

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import json

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from app.config import settings
from app.utils.logger import setup_logger, log_performance

logger = setup_logger(__name__)


class VectorStore:
    """
    Vector store for storing and searching embeddings
    """
    
    def __init__(self, store_path: str = None, model_name: str = None):
        self.store_path = Path(store_path or settings.vector_store_path)
        self.model_name = model_name or settings.embedding_model
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load embedding model {self.model_name}: {e}")
            logger.info("Falling back to TF-IDF vectorization")
            self.embedding_model = None
            self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Initialize storage
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.embeddings_file = self.store_path / "embeddings.pkl"
        self.metadata_file = self.store_path / "metadata.json"
        
        # Load existing data
        self.embeddings = []
        self.metadata = []
        self.load_store()
    
    @log_performance
    def encode_text(self, text: str) -> np.ndarray:
        """
        Encode text into vector embedding
        
        Args:
            text: Input text to encode
            
        Returns:
            Vector embedding as numpy array
        """
        if self.embedding_model:
            return self.embedding_model.encode([text])[0]
        else:
            # Fallback to TF-IDF if transformer model not available
            if not hasattr(self, '_tfidf_fitted'):
                # Need to fit TF-IDF with some data first
                sample_texts = [text, "sample text for fitting"]
                self.tfidf_vectorizer.fit(sample_texts)
                self._tfidf_fitted = True
            
            vector = self.tfidf_vectorizer.transform([text]).toarray()[0]
            return vector
    
    @log_performance
    def add_document(self, text: str, metadata: Dict[str, Any]) -> str:
        """
        Add a document to the vector store
        
        Args:
            text: Document text
            metadata: Associated metadata
            
        Returns:
            Document ID
        """
        try:
            # Generate embedding
            embedding = self.encode_text(text)
            
            # Generate document ID
            doc_id = f"doc_{len(self.embeddings)}"
            
            # Store embedding and metadata
            self.embeddings.append(embedding)
            self.metadata.append({
                "id": doc_id,
                "text": text,
                **metadata
            })
            
            logger.debug(f"Added document {doc_id} to vector store")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding document to vector store: {e}")
            raise
    
    @log_performance
    def search_similar(self, query: str, top_k: int = 5, threshold: float = 0.0) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of (metadata, similarity_score) tuples
        """
        try:
            if not self.embeddings:
                return []
            
            # Encode query
            query_embedding = self.encode_text(query)
            
            # Calculate similarities
            embeddings_matrix = np.array(self.embeddings)
            similarities = cosine_similarity([query_embedding], embeddings_matrix)[0]
            
            # Get top-k similar documents
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                similarity = similarities[idx]
                if similarity >= threshold:
                    results.append((self.metadata[idx], float(similarity)))
            
            logger.debug(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []
    
    @log_performance
    def save_store(self):
        """Save vector store to disk"""
        try:
            # Save embeddings
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings, f)
            
            # Save metadata
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2, default=str)
            
            logger.debug(f"Saved vector store to {self.store_path}")
            
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")
            raise
    
    @log_performance
    def load_store(self):
        """Load vector store from disk"""
        try:
            # Load embeddings
            if self.embeddings_file.exists():
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
            
            # Load metadata
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            
            logger.debug(f"Loaded vector store with {len(self.embeddings)} documents")
            
        except Exception as e:
            logger.warning(f"Could not load existing vector store: {e}")
            self.embeddings = []
            self.metadata = []
    
    def clear_store(self):
        """Clear all data from vector store"""
        self.embeddings = []
        self.metadata = []
        
        # Remove files
        if self.embeddings_file.exists():
            self.embeddings_file.unlink()
        if self.metadata_file.exists():
            self.metadata_file.unlink()
        
        logger.info("Cleared vector store")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "total_documents": len(self.embeddings),
            "embedding_dimension": len(self.embeddings[0]) if self.embeddings else 0,
            "model_name": self.model_name,
            "store_path": str(self.store_path)
        }


class JobMatcher:
    """
    Specialized vector store for job matching
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.logger = setup_logger(__name__)
    
    def add_job(self, job_data: Dict[str, Any]) -> str:
        """
        Add a job to the matching store
        
        Args:
            job_data: Job information dictionary
            
        Returns:
            Job document ID
        """
        # Create searchable text from job data
        job_text = self._create_job_text(job_data)
        
        # Add to vector store
        doc_id = self.vector_store.add_document(job_text, job_data)
        
        return doc_id
    
    def match_resume(self, resume_text: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find jobs matching a resume
        
        Args:
            resume_text: Resume text content
            top_k: Number of top matches to return
            
        Returns:
            List of (job_data, match_score) tuples
        """
        return self.vector_store.search_similar(resume_text, top_k=top_k, threshold=0.1)
    
    def _create_job_text(self, job_data: Dict[str, Any]) -> str:
        """
        Create searchable text representation of job
        
        Args:
            job_data: Job information dictionary
            
        Returns:
            Concatenated job text
        """
        text_parts = []
        
        # Job title and company
        text_parts.append(job_data.get('title', ''))
        text_parts.append(job_data.get('company', ''))
        
        # Description and requirements
        text_parts.append(job_data.get('description', ''))
        
        # Skills and requirements
        if 'skills' in job_data:
            text_parts.extend(job_data['skills'])
        
        if 'requirements' in job_data:
            text_parts.extend(job_data['requirements'])
        
        return ' '.join(filter(None, text_parts))


# Global vector store instance
global_vector_store = VectorStore()