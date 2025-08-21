"""
AI-powered job matching and scoring service
"""

import asyncio
from typing import List, Dict, Any, Tuple
import numpy as np
from datetime import datetime

from app.models.job_schema import Job, Resume
from app.services.resume_parser import ResumeParser
from app.utils.vectorstore import VectorStore
from app.utils.logger import setup_logger, log_async_performance
from app.config import settings

logger = setup_logger(__name__)


class JobMatcher:
    """
    AI-powered job matching and scoring engine
    """
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.vector_store = VectorStore()
        
        # Matching weights for different criteria
        self.weights = {
            'skills_match': 0.4,
            'experience_match': 0.3,
            'description_similarity': 0.2,
            'location_match': 0.05,
            'title_similarity': 0.05
        }
    
    @log_async_performance
    async def match_jobs(self, jobs: List[Job], resume_path: str, top_k: int = 10) -> List[Job]:
        """
        Match and rank jobs based on resume
        
        Args:
            jobs: List of job postings
            resume_path: Path to resume file
            top_k: Number of top matches to return
            
        Returns:
            List of jobs ranked by match score
        """
        try:
            # Parse resume
            resume = self.resume_parser.parse_resume(resume_path)
            logger.info(f"Parsed resume for: {resume.name}")
            
            # Calculate match scores for all jobs
            scored_jobs = []
            
            for job in jobs:
                match_score, match_reasons = await self._calculate_match_score(job, resume)
                
                # Update job with match information
                job.match_score = match_score
                job.match_reasons = match_reasons
                
                scored_jobs.append(job)
            
            # Sort by match score (descending)
            scored_jobs.sort(key=lambda x: x.match_score or 0, reverse=True)
            
            # Return top-k matches
            top_matches = scored_jobs[:top_k]
            
            logger.info(f"Found {len(top_matches)} job matches with scores: {[j.match_score for j in top_matches[:5]]}")
            
            return top_matches
            
        except Exception as e:
            logger.error(f"Error matching jobs: {e}")
            return jobs  # Return original jobs if matching fails
    
    async def _calculate_match_score(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """
        Calculate comprehensive match score between job and resume
        
        Args:
            job: Job posting
            resume: Parsed resume
            
        Returns:
            Tuple of (match_score, match_reasons)
        """
        scores = {}
        reasons = []
        
        # 1. Skills matching
        skills_score, skills_reasons = self._calculate_skills_match(job, resume)
        scores['skills_match'] = skills_score
        reasons.extend(skills_reasons)
        
        # 2. Experience matching
        experience_score, exp_reasons = self._calculate_experience_match(job, resume)
        scores['experience_match'] = experience_score
        reasons.extend(exp_reasons)
        
        # 3. Description similarity (using vector similarity)
        desc_score, desc_reasons = await self._calculate_description_similarity(job, resume)
        scores['description_similarity'] = desc_score
        reasons.extend(desc_reasons)
        
        # 4. Location matching
        location_score, loc_reasons = self._calculate_location_match(job, resume)
        scores['location_match'] = location_score
        reasons.extend(loc_reasons)
        
        # 5. Title similarity
        title_score, title_reasons = self._calculate_title_similarity(job, resume)
        scores['title_similarity'] = title_score
        reasons.extend(title_reasons)
        
        # Calculate weighted final score
        final_score = sum(scores[key] * self.weights[key] for key in scores)
        
        # Normalize to 0-1 range
        final_score = min(max(final_score, 0), 1)
        
        return final_score, reasons[:10]  # Limit reasons to top 10
    
    def _calculate_skills_match(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """Calculate skills matching score"""
        reasons = []
        
        # Get job skills (from job requirements and skills fields)
        job_skills = set()
        job_skills.update([skill.lower() for skill in job.skills])
        job_skills.update([req.lower() for req in job.requirements if len(req.split()) <= 3])
        
        # Get resume skills
        resume_skills = set([skill.lower() for skill in resume.skills])
        resume_technical_skills = set([skill.lower() for skill in resume.technical_skills])
        
        all_resume_skills = resume_skills.union(resume_technical_skills)
        
        if not job_skills or not all_resume_skills:
            return 0.0, ["No skills information available for comparison"]
        
        # Calculate intersection
        matching_skills = job_skills.intersection(all_resume_skills)
        
        if matching_skills:
            # Skills match score
            skills_score = len(matching_skills) / len(job_skills)
            skills_score = min(skills_score, 1.0)  # Cap at 1.0
            
            reasons.append(f"Matching skills: {', '.join(list(matching_skills)[:5])}")
            
            if skills_score > 0.7:
                reasons.append("Excellent skills match")
            elif skills_score > 0.4:
                reasons.append("Good skills match")
            else:
                reasons.append("Partial skills match")
        else:
            skills_score = 0.0
            reasons.append("No direct skills match found")
        
        return skills_score, reasons
    
    def _calculate_experience_match(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """Calculate experience level matching"""
        reasons = []
        
        # Map experience levels to years
        experience_map = {
            'entry_level': (0, 2),
            'associate': (2, 5),
            'mid_senior': (5, 10),
            'director': (10, 15),
            'executive': (15, 30)
        }
        
        job_exp_range = experience_map.get(job.experience_level.value, (0, 30))
        resume_years = resume.years_experience or 0
        
        # Calculate how well resume experience fits job requirements
        if job_exp_range[0] <= resume_years <= job_exp_range[1]:
            exp_score = 1.0
            reasons.append(f"Experience level matches perfectly ({resume_years} years)")
        elif resume_years < job_exp_range[0]:
            # Under-qualified
            gap = job_exp_range[0] - resume_years
            exp_score = max(0, 1 - gap / 5)  # Reduce score based on gap
            reasons.append(f"Slightly under-qualified ({resume_years} vs {job_exp_range[0]}+ years required)")
        else:
            # Over-qualified
            excess = resume_years - job_exp_range[1]
            exp_score = max(0.7, 1 - excess / 10)  # Over-qualification is less penalized
            reasons.append(f"Over-qualified ({resume_years} vs {job_exp_range[1]} years required)")
        
        return exp_score, reasons
    
    async def _calculate_description_similarity(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """Calculate semantic similarity between job description and resume"""
        reasons = []
        
        try:
            # Combine job text
            job_text = f"{job.title} {job.description} {' '.join(job.requirements)}"
            
            # Combine resume text
            resume_text = f"{resume.summary} {' '.join(resume.skills)} {' '.join([exp.get('description', '') for exp in resume.experience])}"
            
            # Use vector store for similarity calculation
            # Add job text to temporary vector store
            temp_vector_store = VectorStore()
            doc_id = temp_vector_store.add_document(job_text, {"type": "job", "id": job.id})
            
            # Search for similarity with resume
            results = temp_vector_store.search_similar(resume_text, top_k=1)
            
            if results:
                similarity_score = results[0][1]  # Get similarity score
                
                if similarity_score > 0.8:
                    reasons.append("Excellent semantic match with job description")
                elif similarity_score > 0.6:
                    reasons.append("Good semantic match with job description")
                elif similarity_score > 0.4:
                    reasons.append("Moderate semantic match with job description")
                else:
                    reasons.append("Limited semantic match with job description")
                
                return similarity_score, reasons
            else:
                return 0.0, ["Could not calculate semantic similarity"]
                
        except Exception as e:
            logger.warning(f"Error calculating description similarity: {e}")
            return 0.0, ["Error in semantic analysis"]
    
    def _calculate_location_match(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """Calculate location matching score"""
        reasons = []
        
        job_location = job.location.lower()
        resume_location = resume.location.lower()
        
        # Remote work gets high score
        if 'remote' in job_location:
            return 1.0, ["Remote position - location flexible"]
        
        # Exact location match
        if job_location == resume_location:
            return 1.0, ["Exact location match"]
        
        # State/region match (simplified)
        job_parts = job_location.split(',')
        resume_parts = resume_location.split(',')
        
        if len(job_parts) > 1 and len(resume_parts) > 1:
            # Check state match
            if job_parts[-1].strip() == resume_parts[-1].strip():
                return 0.8, ["Same state/region"]
        
        # City name match
        if any(part.strip() in resume_location for part in job_parts):
            return 0.6, ["Nearby location"]
        
        return 0.2, ["Different location (may require relocation)"]
    
    def _calculate_title_similarity(self, job: Job, resume: Resume) -> Tuple[float, List[str]]:
        """Calculate job title similarity with resume experience"""
        reasons = []
        
        job_title = job.title.lower()
        
        # Check against experience titles
        for exp in resume.experience:
            exp_title = exp.get('title', '').lower()
            
            # Simple keyword matching
            job_words = set(job_title.split())
            exp_words = set(exp_title.split())
            
            common_words = job_words.intersection(exp_words)
            
            if common_words:
                similarity = len(common_words) / max(len(job_words), len(exp_words))
                
                if similarity > 0.5:
                    reasons.append(f"Similar role: {exp.get('title', '')}")
                    return similarity, reasons
        
        # Check for common role keywords
        role_keywords = ['engineer', 'developer', 'analyst', 'manager', 'specialist', 'lead', 'senior']
        
        for keyword in role_keywords:
            if keyword in job_title:
                for exp in resume.experience:
                    if keyword in exp.get('title', '').lower():
                        reasons.append(f"Same role type: {keyword}")
                        return 0.6, reasons
        
        return 0.0, ["No similar role experience found"]
    
    async def rank_candidates(self, candidates: List[Dict[str, Any]], job: Job) -> List[Dict[str, Any]]:
        """
        Rank candidates for a specific job
        
        Args:
            candidates: List of candidate information with resume paths
            job: Job posting to match against
            
        Returns:
            List of candidates ranked by match score
        """
        scored_candidates = []
        
        for candidate in candidates:
            try:
                resume_path = candidate.get('resume_path')
                if not resume_path:
                    continue
                
                # Parse candidate resume
                resume = self.resume_parser.parse_resume(resume_path)
                
                # Calculate match score
                match_score, match_reasons = await self._calculate_match_score(job, resume)
                
                # Add scoring information
                candidate_with_score = {
                    **candidate,
                    'match_score': match_score,
                    'match_reasons': match_reasons,
                    'resume_summary': {
                        'name': resume.name,
                        'skills': resume.skills[:10],  # Top 10 skills
                        'years_experience': resume.years_experience
                    }
                }
                
                scored_candidates.append(candidate_with_score)
                
            except Exception as e:
                logger.warning(f"Error scoring candidate {candidate.get('name', 'Unknown')}: {e}")
                continue
        
        # Sort by match score (descending)
        scored_candidates.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        return scored_candidates
    
    def get_match_insights(self, job: Job, resume: Resume) -> Dict[str, Any]:
        """
        Get detailed insights about a job-resume match
        
        Args:
            job: Job posting
            resume: Parsed resume
            
        Returns:
            Dictionary with detailed match insights
        """
        insights = {
            'overall_score': job.match_score or 0,
            'match_reasons': job.match_reasons or [],
            'skill_analysis': {},
            'experience_analysis': {},
            'recommendations': []
        }
        
        # Skill analysis
        job_skills = set([skill.lower() for skill in job.skills])
        resume_skills = set([skill.lower() for skill in resume.skills])
        
        matching_skills = job_skills.intersection(resume_skills)
        missing_skills = job_skills.difference(resume_skills)
        
        insights['skill_analysis'] = {
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skill_match_percentage': len(matching_skills) / len(job_skills) if job_skills else 0
        }
        
        # Experience analysis
        insights['experience_analysis'] = {
            'candidate_years': resume.years_experience,
            'job_level': job.experience_level.value,
            'experience_match': 'good' if job.match_score and job.match_score > 0.7 else 'needs_improvement'
        }
        
        # Recommendations
        if missing_skills:
            insights['recommendations'].append(f"Consider highlighting experience with: {', '.join(list(missing_skills)[:3])}")
        
        if insights['experience_analysis']['experience_match'] == 'needs_improvement':
            insights['recommendations'].append("Consider emphasizing relevant experience and achievements")
        
        return insights