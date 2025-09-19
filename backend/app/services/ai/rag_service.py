from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List, Dict, Optional
from app.core.config import settings
import pickle
import os

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.vector_store = None
        self.vector_store_path = "ai_models/vector_stores/job_knowledge_base"
        
    def create_knowledge_base(self, documents: List[str], metadata: List[Dict] = None):
        """Create a knowledge base from documents"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        # Convert strings to Document objects
        docs = []
        for i, doc in enumerate(documents):
            meta = metadata[i] if metadata and i < len(metadata) else {}
            docs.append(Document(page_content=doc, metadata=meta))
        
        # Split documents into chunks
        texts = text_splitter.split_documents(docs)
        
        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)
        
        # Save the vector store
        self._save_vector_store()
    
    def load_knowledge_base(self) -> bool:
        """Load existing knowledge base"""
        try:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings
                )
                return True
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
        return False
    
    def search_similar_jobs(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar jobs using vector similarity"""
        if not self.vector_store:
            if not self.load_knowledge_base():
                return []
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            results = []
            
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance_score": "high"  # FAISS doesn't return scores by default
                })
            
            return results
        except Exception as e:
            print(f"Error searching similar jobs: {e}")
            return []
    
    def search_similar_jobs_with_score(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar jobs with similarity scores"""
        if not self.vector_store:
            if not self.load_knowledge_base():
                return []
        
        try:
            docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
            results = []
            
            for doc, score in docs_with_scores:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": float(score),
                    "relevance": "high" if score < 0.3 else "medium" if score < 0.6 else "low"
                })
            
            return results
        except Exception as e:
            print(f"Error searching similar jobs with scores: {e}")
            return []
    
    def add_job_to_knowledge_base(self, job_description: str, job_metadata: Dict):
        """Add a single job to the existing knowledge base"""
        if not self.vector_store:
            if not self.load_knowledge_base():
                # Create new knowledge base if none exists
                self.create_knowledge_base([job_description], [job_metadata])
                return
        
        try:
            # Create document
            doc = Document(page_content=job_description, metadata=job_metadata)
            
            # Add to existing vector store
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            texts = text_splitter.split_documents([doc])
            self.vector_store.add_documents(texts)
            
            # Save updated vector store
            self._save_vector_store()
            
        except Exception as e:
            print(f"Error adding job to knowledge base: {e}")
    
    def find_relevant_experience(self, user_experience: List[str], job_description: str) -> List[Dict]:
        """Find user experiences most relevant to a job description"""
        if not user_experience:
            return []
        
        try:
            # Create temporary vector store with user experience
            experience_docs = [
                Document(page_content=exp, metadata={"type": "experience", "index": i})
                for i, exp in enumerate(user_experience)
            ]
            
            temp_store = FAISS.from_documents(experience_docs, self.embeddings)
            
            # Search for experiences similar to job description
            relevant_docs = temp_store.similarity_search_with_score(job_description, k=3)
            
            results = []
            for doc, score in relevant_docs:
                results.append({
                    "experience": doc.page_content,
                    "relevance_score": float(score),
                    "index": doc.metadata.get("index", 0)
                })
            
            return results
            
        except Exception as e:
            print(f"Error finding relevant experience: {e}")
            return []
    
    def _save_vector_store(self):
        """Save vector store to disk"""
        try:
            if self.vector_store:
                os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
                self.vector_store.save_local(self.vector_store_path)
        except Exception as e:
            print(f"Error saving vector store: {e}")
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get statistics about the knowledge base"""
        if not self.vector_store:
            if not self.load_knowledge_base():
                return {"total_documents": 0, "status": "empty"}
        
        try:
            # Get the total number of documents in the vector store
            total_docs = self.vector_store.index.ntotal
            
            return {
                "total_documents": total_docs,
                "status": "loaded",
                "embedding_dimension": 1536,  # OpenAI embedding dimension
                "vector_store_type": "FAISS"
            }
        except Exception as e:
            return {"total_documents": 0, "status": f"error: {e}"}