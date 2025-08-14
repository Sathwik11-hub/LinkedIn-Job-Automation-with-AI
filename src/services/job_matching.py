"""RAG-based job matching service using FAISS and sentence transformers."""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

from ..core import LoggerMixin, get_settings
from ..models import JobPosting, ResumeData, JobMatch


class JobMatchingService(LoggerMixin):
    """Job matching service using RAG with FAISS vector database."""
    
    def __init__(self):
        self.settings = get_settings()
        self.embedding_model = None
        self.vector_db = None
        self.job_metadata = {}
        self._load_models()
        
    def _load_models(self):
        """Load embedding model and vector database."""
        try:
            self.logger.info(f"Loading embedding model: {self.settings.embedding_model}")
            self.embedding_model = SentenceTransformer(self.settings.embedding_model)
            self.logger.info("Embedding model loaded successfully")
            
            # Try to load existing vector database
            self._load_vector_db()
            
        except Exception as e:
            self.logger.error(f"Failed to load models: {str(e)}")
            raise
    
    def _load_vector_db(self):
        """Load existing vector database if available."""
        db_path = Path(self.settings.jobs_data_path) / "vector_db.faiss"
        metadata_path = Path(self.settings.jobs_data_path) / "job_metadata.pkl"
        
        if db_path.exists() and metadata_path.exists():
            try:
                self.vector_db = faiss.read_index(str(db_path))
                with open(metadata_path, 'rb') as f:
                    self.job_metadata = pickle.load(f)
                self.logger.info(f"Loaded vector database with {self.vector_db.ntotal} jobs")
            except Exception as e:
                self.logger.warning(f"Failed to load existing vector database: {str(e)}")
                self._initialize_vector_db()
        else:
            self._initialize_vector_db()
    
    def _initialize_vector_db(self):
        """Initialize new vector database."""
        # Get embedding dimension
        sample_text = "sample text for dimension"
        sample_embedding = self.embedding_model.encode([sample_text])
        dimension = sample_embedding.shape[1]
        
        # Create FAISS index
        self.vector_db = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        self.job_metadata = {}
        self.logger.info(f"Initialized new vector database with dimension {dimension}")
    
    def add_jobs_to_index(self, jobs: List[JobPosting]):
        """Add jobs to the vector database."""
        if not jobs:
            return
        
        self.logger.info(f"Adding {len(jobs)} jobs to vector index")
        
        # Prepare job texts for embedding
        job_texts = []
        job_ids = []
        
        for job in jobs:
            # Combine job title, description, and requirements for embedding
            job_text = f"{job.title} {job.description}"
            if job.requirements:
                job_text += f" {job.requirements}"
                
            job_texts.append(job_text)
            job_ids.append(job.job_id)
            
            # Store job metadata
            self.job_metadata[job.job_id] = {
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'url': job.url,
                'description': job.description,
                'requirements': job.requirements,
                'experience_level': job.experience_level.value if job.experience_level else None,
                'posted_date': job.posted_date.isoformat() if job.posted_date else None
            }
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(job_texts, show_progress_bar=True)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS index
        self.vector_db.add(embeddings.astype('float32'))
        
        # Save updated index and metadata
        self._save_vector_db()
        
        self.logger.info(f"Successfully added {len(jobs)} jobs to index. Total jobs: {self.vector_db.ntotal}")
    
    def _save_vector_db(self):
        """Save vector database and metadata to disk."""
        try:
            db_path = Path(self.settings.jobs_data_path) / "vector_db.faiss"
            metadata_path = Path(self.settings.jobs_data_path) / "job_metadata.pkl"
            
            faiss.write_index(self.vector_db, str(db_path))
            with open(metadata_path, 'wb') as f:
                pickle.dump(self.job_metadata, f)
                
            self.logger.info("Vector database saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save vector database: {str(e)}")
    
    def match_jobs(self, resume_data: ResumeData, top_k: int = 20) -> List[JobMatch]:
        """Match jobs to resume using vector similarity."""
        if self.vector_db.ntotal == 0:
            self.logger.warning("No jobs in vector database")
            return []
        
        self.logger.info(f"Matching jobs for resume with {len(resume_data.skills)} skills")
        
        # Create resume text for embedding
        resume_text = self._create_resume_text(resume_data)
        
        # Generate resume embedding
        resume_embedding = self.embedding_model.encode([resume_text])
        resume_embedding = resume_embedding / np.linalg.norm(resume_embedding, axis=1, keepdims=True)
        
        # Search for similar jobs
        similarities, indices = self.vector_db.search(resume_embedding.astype('float32'), top_k)
        
        # Create job matches
        matches = []
        for i, (similarity, job_idx) in enumerate(zip(similarities[0], indices[0])):
            if job_idx == -1:  # No more results
                break
                
            # Get job metadata
            job_id = list(self.job_metadata.keys())[job_idx]
            job_meta = self.job_metadata[job_id]
            
            # Calculate detailed match information
            match_details = self._calculate_match_details(resume_data, job_meta)
            
            job_match = JobMatch(
                job_id=job_id,
                similarity_score=float(similarity),
                matched_skills=match_details['matched_skills'],
                missing_skills=match_details['missing_skills'],
                recommendation=match_details['recommendation'],
                confidence=match_details['confidence']
            )
            
            matches.append(job_match)
        
        # Sort by similarity score
        matches.sort(key=lambda x: x.similarity_score, reverse=True)
        
        self.logger.info(f"Found {len(matches)} job matches")
        return matches
    
    def _create_resume_text(self, resume_data: ResumeData) -> str:
        """Create text representation of resume for embedding."""
        text_parts = []
        
        # Add skills
        if resume_data.skills:
            text_parts.append(f"Skills: {' '.join(resume_data.skills)}")
        
        # Add summary
        if resume_data.summary:
            text_parts.append(f"Summary: {resume_data.summary}")
        
        # Add experience
        for exp in resume_data.experience:
            if 'title' in exp:
                text_parts.append(f"Experience: {exp['title']}")
            if 'description' in exp:
                text_parts.append(exp['description'])
        
        # Add education
        for edu in resume_data.education:
            if 'degree' in edu:
                text_parts.append(f"Education: {edu['degree']}")
        
        return ' '.join(text_parts)
    
    def _calculate_match_details(self, resume_data: ResumeData, job_meta: Dict) -> Dict:
        """Calculate detailed matching information."""
        # Extract skills from job description
        job_skills = self._extract_job_skills(job_meta['description'])
        resume_skills_lower = [skill.lower() for skill in resume_data.skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Find matched and missing skills
        matched_skills = []
        missing_skills = []
        
        for job_skill in job_skills:
            if job_skill.lower() in resume_skills_lower:
                matched_skills.append(job_skill)
            else:
                missing_skills.append(job_skill)
        
        # Calculate skill match ratio
        skill_match_ratio = len(matched_skills) / len(job_skills) if job_skills else 0
        
        # Generate recommendation
        if skill_match_ratio >= 0.8:
            recommendation = "Highly Recommended - Excellent skill match"
        elif skill_match_ratio >= 0.6:
            recommendation = "Recommended - Good skill match"
        elif skill_match_ratio >= 0.4:
            recommendation = "Consider - Moderate skill match"
        else:
            recommendation = "Not Recommended - Poor skill match"
        
        # Calculate confidence based on multiple factors
        confidence = skill_match_ratio * 0.7  # 70% weight on skills
        
        # Add experience level matching (if available)
        if job_meta.get('experience_level') and resume_data.experience:
            # Simple heuristic: more experience = higher confidence for senior roles
            exp_years = len(resume_data.experience)  # Rough estimate
            if job_meta['experience_level'] in ['Entry level', 'Associate'] and exp_years <= 3:
                confidence += 0.2
            elif job_meta['experience_level'] in ['Mid-Senior level'] and 2 <= exp_years <= 8:
                confidence += 0.2
            elif job_meta['experience_level'] in ['Director', 'Executive'] and exp_years >= 5:
                confidence += 0.2
        
        confidence = min(confidence, 1.0)  # Cap at 1.0
        
        return {
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendation': recommendation,
            'confidence': confidence
        }
    
    def _extract_job_skills(self, job_description: str) -> List[str]:
        """Extract skills mentioned in job description."""
        if not job_description:
            return []
        
        # Common technical skills (same as in resume parser)
        skill_keywords = [
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'xml', 'json',
            
            # Frameworks and libraries
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'nodejs', 'express',
            'jquery', 'bootstrap', 'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'terraform',
            
            # General skills
            'machine learning', 'deep learning', 'ai', 'nlp', 'data science', 'agile', 'scrum'
        ]
        
        found_skills = []
        job_text_lower = job_description.lower()
        
        for skill in skill_keywords:
            if skill.lower() in job_text_lower:
                # Check for word boundaries to avoid partial matches
                import re
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', job_text_lower):
                    found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def get_job_by_id(self, job_id: str) -> Optional[Dict]:
        """Get job metadata by ID."""
        return self.job_metadata.get(job_id)
    
    def clear_index(self):
        """Clear the vector database."""
        self._initialize_vector_db()
        self.logger.info("Vector database cleared")
    
    def get_index_stats(self) -> Dict:
        """Get statistics about the vector database."""
        return {
            'total_jobs': self.vector_db.ntotal if self.vector_db else 0,
            'dimension': self.vector_db.d if self.vector_db else 0,
            'model_name': self.settings.embedding_model
        }