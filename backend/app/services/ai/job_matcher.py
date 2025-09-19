from typing import Dict, List
from app.services.ai.llm_service import LLMService
from app.services.ai.resume_parser import ResumeParser
from app.services.ai.rag_service import RAGService
from app.models.job import Job
from app.models.user import User
import asyncio

class JobMatcher:
    """AI-powered job matching service"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.resume_parser = ResumeParser()
        self.rag_service = RAGService()
    
    async def calculate_job_match_score(
        self, 
        job: Job, 
        user_skills: List[str], 
        user_experience: List[str] = None
    ) -> Dict:
        """Calculate comprehensive job match score"""
        
        if not job.description:
            return {
                "overall_score": 0,
                "skill_match_score": 0,
                "experience_match_score": 0,
                "details": {"error": "Job description not available"}
            }
        
        try:
            # Analyze job requirements
            job_analysis = await self.llm_service.extract_job_requirements(job.description)
            
            # Calculate skill match
            skill_match = await self.llm_service.analyze_job_fit(job.description, user_skills)
            
            # Find relevant experience using RAG
            experience_relevance = []
            if user_experience:
                experience_relevance = self.rag_service.find_relevant_experience(
                    user_experience, job.description
                )
            
            # Calculate scores
            skill_score = skill_match.get("match_score", 0)
            experience_score = self._calculate_experience_score(experience_relevance)
            
            # Weight the scores (60% skills, 40% experience)
            overall_score = (skill_score * 0.6) + (experience_score * 0.4)
            
            return {
                "overall_score": round(overall_score, 1),
                "skill_match_score": skill_score,
                "experience_match_score": experience_score,
                "matching_skills": skill_match.get("matching_skills", []),
                "missing_skills": skill_match.get("missing_skills", []),
                "relevant_experience": [exp["experience"] for exp in experience_relevance[:2]],
                "job_requirements": job_analysis,
                "recommendations": skill_match.get("recommendations", [])
            }
            
        except Exception as e:
            print(f"Error calculating job match score: {e}")
            return {
                "overall_score": 0,
                "skill_match_score": 0,
                "experience_match_score": 0,
                "details": {"error": str(e)}
            }
    
    def _calculate_experience_score(self, experience_relevance: List[Dict]) -> float:
        """Calculate experience match score based on relevance"""
        if not experience_relevance:
            return 50.0  # Neutral score if no experience data
        
        # Convert similarity scores to match scores (lower similarity = higher match)
        scores = []
        for exp in experience_relevance:
            relevance_score = exp.get("relevance_score", 1.0)
            # Convert to 0-100 scale (lower similarity distance = higher score)
            match_score = max(0, 100 - (relevance_score * 100))
            scores.append(match_score)
        
        # Return average of top experiences
        return sum(scores) / len(scores) if scores else 50.0
    
    async def rank_jobs_for_user(self, jobs: List[Job], user: User) -> List[Dict]:
        """Rank jobs by match score for a specific user"""
        
        # Parse user resume to get skills and experience
        user_skills = []
        user_experience = []
        
        if user.resume_path:
            try:
                resume_text = self.resume_parser.extract_text_from_pdf(user.resume_path)
                resume_data = self.resume_parser.parse_resume(resume_text)
                user_skills = resume_data.get("skills", [])
                user_experience = [
                    f"{exp.get('title', '')} at {exp.get('company', '')}: {exp.get('description', '')}"
                    for exp in resume_data.get("experience", [])
                ]
            except Exception as e:
                print(f"Error parsing user resume: {e}")
        
        # Calculate match scores for all jobs
        ranked_jobs = []
        
        for job in jobs:
            try:
                match_result = await self.calculate_job_match_score(
                    job, user_skills, user_experience
                )
                
                ranked_jobs.append({
                    "job": job,
                    "match_score": match_result["overall_score"],
                    "match_details": match_result,
                    "priority": self._get_priority_level(match_result["overall_score"])
                })
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"Error ranking job {job.id}: {e}")
                ranked_jobs.append({
                    "job": job,
                    "match_score": 0,
                    "match_details": {"error": str(e)},
                    "priority": "low"
                })
        
        # Sort by match score (highest first)
        ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        return ranked_jobs
    
    def _get_priority_level(self, score: float) -> str:
        """Get priority level based on match score"""
        if score >= 80:
            return "high"
        elif score >= 60:
            return "medium"
        elif score >= 40:
            return "low"
        else:
            return "very_low"
    
    async def get_job_application_strategy(self, job: Job, user: User) -> Dict:
        """Get AI-recommended application strategy for a job"""
        
        try:
            # Get job match details
            user_skills = []
            if user.resume_path:
                resume_text = self.resume_parser.extract_text_from_pdf(user.resume_path)
                resume_data = self.resume_parser.parse_resume(resume_text)
                user_skills = resume_data.get("skills", [])
            
            match_result = await self.calculate_job_match_score(job, user_skills)
            
            # Generate strategy based on match score
            strategy = {
                "application_priority": self._get_priority_level(match_result["overall_score"]),
                "match_score": match_result["overall_score"],
                "key_selling_points": match_result.get("matching_skills", [])[:3],
                "skills_to_emphasize": match_result.get("matching_skills", []),
                "potential_concerns": match_result.get("missing_skills", []),
                "cover_letter_focus": [],
                "application_timing": "immediate" if match_result["overall_score"] >= 70 else "standard"
            }
            
            # Add cover letter focus points
            if match_result["overall_score"] >= 70:
                strategy["cover_letter_focus"] = [
                    "Highlight strong skill alignment",
                    "Emphasize relevant experience",
                    "Show enthusiasm for the role"
                ]
            else:
                strategy["cover_letter_focus"] = [
                    "Address skill gaps proactively", 
                    "Highlight transferable skills",
                    "Show willingness to learn"
                ]
            
            return strategy
            
        except Exception as e:
            print(f"Error getting application strategy: {e}")
            return {
                "application_priority": "low",
                "match_score": 0,
                "error": str(e)
            }
    
    async def find_similar_jobs(self, job: Job, limit: int = 5) -> List[Dict]:
        """Find jobs similar to the given job using RAG"""
        
        if not job.description:
            return []
        
        try:
            # Search for similar jobs in the knowledge base
            similar_jobs = self.rag_service.search_similar_jobs_with_score(
                job.description, k=limit
            )
            
            return [
                {
                    "content": job_data["content"],
                    "similarity_score": job_data["similarity_score"],
                    "metadata": job_data.get("metadata", {}),
                    "relevance": job_data.get("relevance", "unknown")
                }
                for job_data in similar_jobs
            ]
            
        except Exception as e:
            print(f"Error finding similar jobs: {e}")
            return []