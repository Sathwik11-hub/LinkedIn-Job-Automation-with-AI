from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from app.models.user import User
from app.schemas.application import ApplicationCreate
from app.services.automation.linkedin_bot import LinkedInBot
from app.services.ai.llm_service import LLMService
from app.services.ai.resume_parser import ResumeParser
import asyncio

class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.resume_parser = ResumeParser()
    
    async def create_application(self, application_data: ApplicationCreate) -> Application:
        """Create a new job application"""
        # Get job and user information
        job = self.db.query(Job).filter(Job.id == application_data.job_id).first()
        user = self.db.query(User).filter(User.id == application_data.user_id).first()
        
        if not job or not user:
            raise ValueError("Job or user not found")
        
        # Generate cover letter if not provided
        cover_letter = application_data.cover_letter
        if not cover_letter and user.resume_path:
            cover_letter = await self._generate_cover_letter(job, user)
        
        # Create application record
        db_application = Application(
            user_id=application_data.user_id,
            job_id=application_data.job_id,
            cover_letter=cover_letter,
            notes=application_data.notes,
            custom_resume_path=application_data.custom_resume_path,
            status=ApplicationStatus.PENDING
        )
        
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        
        return db_application
    
    async def batch_apply(self, job_ids: List[int], user_id: int = 1) -> List[dict]:
        """Apply to multiple jobs automatically"""
        results = []
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return [{"error": "User not found"}]
        
        # Initialize LinkedIn bot
        linkedin_bot = LinkedInBot({
            "email": user.linkedin_email or "",
            "password": user.linkedin_password or ""
        })
        
        try:
            for job_id in job_ids:
                try:
                    result = await self._apply_to_single_job(job_id, user, linkedin_bot)
                    results.append(result)
                    
                    # Add delay between applications
                    await asyncio.sleep(30)  # 30 second delay
                    
                except Exception as e:
                    results.append({
                        "job_id": job_id,
                        "success": False,
                        "error": str(e)
                    })
            
        finally:
            await linkedin_bot.close()
        
        return results
    
    async def _apply_to_single_job(self, job_id: int, user: User, linkedin_bot: LinkedInBot) -> dict:
        """Apply to a single job using automation"""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            return {"job_id": job_id, "success": False, "error": "Job not found"}
        
        # Check if already applied
        existing_app = self.db.query(Application).filter(
            Application.job_id == job_id,
            Application.user_id == user.id
        ).first()
        
        if existing_app:
            return {"job_id": job_id, "success": False, "error": "Already applied"}
        
        # Generate cover letter
        cover_letter = await self._generate_cover_letter(job, user)
        
        # Apply through LinkedIn bot
        application_result = await linkedin_bot.apply_to_job(
            job_url=job.job_url,
            cover_letter=cover_letter
        )
        
        # Create application record
        status = ApplicationStatus.APPLIED if application_result.get("success") else ApplicationStatus.PENDING
        
        db_application = Application(
            user_id=user.id,
            job_id=job_id,
            cover_letter=cover_letter,
            status=status,
            automated=True
        )
        
        self.db.add(db_application)
        self.db.commit()
        
        return {
            "job_id": job_id,
            "success": application_result.get("success", False),
            "application_id": db_application.id,
            "message": application_result.get("message", "")
        }
    
    async def _generate_cover_letter(self, job: Job, user: User) -> str:
        """Generate a cover letter for the job application"""
        # Parse resume if available
        resume_content = ""
        if user.resume_path:
            try:
                resume_text = self.resume_parser.extract_text_from_pdf(user.resume_path)
                resume_data = self.resume_parser.parse_resume(resume_text)
                
                # Create a summary of resume content
                skills = ", ".join(resume_data.get("skills", []))
                experience = resume_data.get("experience", [])
                exp_summary = "; ".join([f"{exp.get('title', '')} at {exp.get('company', '')}" 
                                       for exp in experience[:3]])
                
                resume_content = f"Skills: {skills}\nExperience: {exp_summary}"
                
            except Exception as e:
                print(f"Error parsing resume: {e}")
                resume_content = "Resume parsing failed"
        
        # Generate cover letter using AI
        job_description = f"Title: {job.title}\nCompany: {job.company}\nDescription: {job.description or 'No description available'}"
        
        cover_letter = await self.llm_service.generate_cover_letter(
            job_description=job_description,
            resume_content=resume_content,
            user_name=user.full_name or "Job Applicant"
        )
        
        return cover_letter
    
    def get_user_applications(self, user_id: int, status_filter: Optional[ApplicationStatus] = None) -> List[Application]:
        """Get applications for a specific user"""
        query = self.db.query(Application).filter(Application.user_id == user_id)
        
        if status_filter:
            query = query.filter(Application.status == status_filter)
        
        return query.order_by(Application.application_date.desc()).all()
    
    def update_application_status(self, application_id: int, status: ApplicationStatus, notes: str = "") -> Optional[Application]:
        """Update application status"""
        application = self.db.query(Application).filter(Application.id == application_id).first()
        
        if application:
            application.status = status
            if notes:
                application.notes = notes
            
            self.db.commit()
            self.db.refresh(application)
        
        return application