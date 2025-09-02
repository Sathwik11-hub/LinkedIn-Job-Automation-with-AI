from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.job import Job
from app.schemas.job import JobSearchParams, JobCreate
from app.services.automation.linkedin_bot import LinkedInBot
from app.services.ai.llm_service import LLMService
import asyncio

class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
    
    async def search_jobs(self, search_params: JobSearchParams) -> List[Job]:
        """Search for jobs based on parameters"""
        # First, search in local database
        query = self.db.query(Job).filter(Job.is_active == True)
        
        if search_params.location:
            query = query.filter(Job.location.ilike(f"%{search_params.location}%"))
        
        if search_params.job_type:
            query = query.filter(Job.job_type == search_params.job_type)
        
        if search_params.remote_option is not None:
            query = query.filter(Job.remote_option == search_params.remote_option)
        
        if search_params.salary_min:
            query = query.filter(Job.salary_min >= search_params.salary_min)
        
        # Search by keywords in title and description
        if search_params.keywords:
            keyword_filter = Job.title.ilike(f"%{search_params.keywords}%") | \
                           Job.description.ilike(f"%{search_params.keywords}%")
            query = query.filter(keyword_filter)
        
        local_jobs = query.limit(50).all()
        
        # If we don't have enough local jobs, scrape LinkedIn
        if len(local_jobs) < 10:
            await self._scrape_and_save_jobs(search_params)
            # Re-run the query to get newly scraped jobs
            local_jobs = query.limit(50).all()
        
        return local_jobs
    
    async def _scrape_and_save_jobs(self, search_params: JobSearchParams):
        """Scrape jobs from LinkedIn and save to database"""
        try:
            linkedin_bot = LinkedInBot({})
            jobs_data = await linkedin_bot.search_jobs(
                keywords=search_params.keywords,
                location=search_params.location or "",
                job_type=search_params.job_type or "",
                experience_level=search_params.experience_level or ""
            )
            
            for job_data in jobs_data:
                # Check if job already exists
                existing_job = self.db.query(Job).filter(
                    Job.linkedin_job_id == job_data.get("linkedin_job_id")
                ).first()
                
                if not existing_job and job_data.get("linkedin_job_id"):
                    # Create new job record
                    new_job = Job(
                        title=job_data.get("title", ""),
                        company=job_data.get("company", ""),
                        location=job_data.get("location", ""),
                        job_url=job_data.get("job_url", ""),
                        linkedin_job_id=job_data.get("linkedin_job_id", ""),
                        # Set defaults for other fields
                        job_type="full-time",
                        remote_option=False,
                        is_active=True
                    )
                    
                    self.db.add(new_job)
            
            self.db.commit()
            await linkedin_bot.close()
            
        except Exception as e:
            print(f"Error scraping jobs: {e}")
    
    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """Get a specific job by ID"""
        return self.db.query(Job).filter(Job.id == job_id).first()
    
    def create_job(self, job_data: JobCreate) -> Job:
        """Create a new job posting"""
        db_job = Job(**job_data.dict())
        self.db.add(db_job)
        self.db.commit()
        self.db.refresh(db_job)
        return db_job
    
    async def analyze_job_requirements(self, job_id: int) -> dict:
        """Analyze job requirements using AI"""
        job = self.get_job_by_id(job_id)
        if not job or not job.description:
            return {}
        
        return await self.llm_service.extract_job_requirements(job.description)