"""
Main API routes for AutoAgentHire application.
Handles job automation, user management, and application tracking.
"""
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from pydantic import BaseModel, EmailStr, Field
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["api"])


# ==========================================
# Request/Response Models
# ==========================================

class UserProfileCreate(BaseModel):
    """User profile creation model."""
    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    linkedin_email: EmailStr
    linkedin_password: str = Field(..., min_length=6)
    job_keywords: List[str] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    job_type: str = Field(default="Remote", pattern="^(Remote|On-site|Hybrid|Any)$")
    experience_level: str = Field(default="Mid-level")
    skills: List[str] = Field(default_factory=list)
    gemini_api_key: Optional[str] = None


class JobSearchRequest(BaseModel):
    """Job search request model."""
    keywords: str = Field(..., min_length=1)
    location: str = Field(default="Remote")
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    easy_apply_only: bool = True
    max_results: int = Field(default=50, le=100)
    linkedin_email: Optional[str] = None
    linkedin_password: Optional[str] = None
    submit_applications: bool = False  # Safety flag


class ApplicationSubmitRequest(BaseModel):
    """Application submission request."""
    job_id: str
    cover_letter: Optional[str] = None
    additional_answers: Optional[Dict[str, str]] = None


class AgentRunRequest(BaseModel):
    """Full agent automation run request."""
    user_profile: UserProfileCreate
    search_criteria: JobSearchRequest
    auto_submit: bool = False
    min_match_score: float = Field(default=0.7, ge=0, le=1)


# ==========================================
# Global State Management
# ==========================================

class ApplicationState:
    """Tracks the current state of agent execution."""
    
    def __init__(self):
        self.status = "idle"  # idle, running, paused, completed, failed
        self.current_phase = ""  # login, searching, applying, etc.
        self.jobs_found = 0
        self.applications_submitted = 0
        self.applications_previewed = 0
        self.errors = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.logs = []
    
    def reset(self):
        self.__init__()
    
    def add_log(self, level: str, message: str):
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "phase": self.current_phase,
            "jobs_found": self.jobs_found,
            "applications_submitted": self.applications_submitted,
            "applications_previewed": self.applications_previewed,
            "errors": self.errors,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "logs": self.logs[-20:]  # Last 20 logs
        }


# Global state instance
app_state = ApplicationState()


# ==========================================
# Routes
# ==========================================

@router.post("/run-agent")
async def run_agent(
    background_tasks: BackgroundTasks,
    request: Optional[Dict[str, Any]] = None
):
    """
    Start the automated job application agent.
    
    This endpoint triggers the full workflow:
    1. Login to LinkedIn
    2. Search for jobs matching criteria
    3. Evaluate job matches using AI
    4. Preview or submit applications
    """
    if app_state.status == "running":
        raise HTTPException(400, "Agent is already running")
    
    try:
        data = request or {}
        
        # Reset state
        app_state.reset()
        app_state.status = "running"
        app_state.start_time = datetime.now()
        app_state.add_log("INFO", "Agent started")
        
        # Run in background
        background_tasks.add_task(execute_agent_workflow, data)
        
        return {
            "status": "started",
            "message": "Agent workflow started in background",
            "job_id": "agent-run-1"
        }
        
    except Exception as e:
        logger.error(f"Failed to start agent: {e}")
        app_state.status = "failed"
        app_state.add_log("ERROR", str(e))
        raise HTTPException(500, f"Failed to start agent: {e}")


@router.get("/agent/status")
async def get_agent_status():
    """Get current agent execution status."""
    return {
        "status": app_state.status,
        "detail": app_state.to_dict()
    }


@router.post("/agent/pause")
async def pause_agent():
    """Pause the running agent."""
    if app_state.status != "running":
        raise HTTPException(400, "Agent is not running")
    
    app_state.status = "paused"
    app_state.add_log("INFO", "Agent paused by user")
    
    return {"status": "paused"}


@router.post("/agent/resume")
async def resume_agent():
    """Resume a paused agent."""
    if app_state.status != "paused":
        raise HTTPException(400, "Agent is not paused")
    
    app_state.status = "running"
    app_state.add_log("INFO", "Agent resumed by user")
    
    return {"status": "resumed"}


@router.post("/agent/stop")
async def stop_agent():
    """Stop the running agent."""
    if app_state.status not in ["running", "paused"]:
        raise HTTPException(400, "Agent is not running or paused")
    
    app_state.status = "stopped"
    app_state.end_time = datetime.now()
    app_state.add_log("INFO", "Agent stopped by user")
    
    return {"status": "stopped"}


@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    user_email: str = Form(...)
):
    """
    Upload and process resume for the user.
    Extracts text and stores for AI processing.
    """
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(400, "Only PDF, DOCX, and TXT files are supported")
    
    try:
        # Save file
        upload_dir = "uploads/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{user_email}_{file.filename}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract text
        from backend.parsers.resume_parser import extract_resume_text
        resume_text = extract_resume_text(file_path)
        
        # Generate summary using Gemini
        from backend.llm.gemini_service import get_gemini_service
        gemini = get_gemini_service()
        summary = gemini.generate_resume_summary(resume_text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_path": file_path,
            "text_length": len(resume_text),
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(500, f"Failed to process resume: {e}")


@router.post("/generate-cover-letter")
async def generate_cover_letter(
    job_title: str = Form(...),
    company: str = Form(...),
    job_description: str = Form(...),
    user_name: str = Form(...),
    resume_text: str = Form(...)
):
    """
    Generate AI-powered cover letter for a job application.
    """
    try:
        from backend.llm.gemini_service import get_gemini_service
        gemini = get_gemini_service()
        
        cover_letter = gemini.generate_cover_letter(
            job_title=job_title,
            company=company,
            job_description=job_description,
            resume_text=resume_text,
            user_name=user_name
        )
        
        # Save cover letter
        upload_dir = "uploads/cover_letters"
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{user_name}_{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = os.path.join(upload_dir, filename)
        
        with open(file_path, "w") as f:
            f.write(cover_letter)
        
        return {
            "status": "success",
            "cover_letter": cover_letter,
            "file_path": file_path
        }
        
    except Exception as e:
        logger.error(f"Error generating cover letter: {e}")
        raise HTTPException(500, f"Failed to generate cover letter: {e}")


@router.post("/answer-question")
async def answer_application_question(
    question: str = Form(...),
    job_title: str = Form(...),
    company: str = Form(...),
    resume_text: str = Form(...),
    max_words: Optional[int] = Form(None)
):
    """
    Generate intelligent answer to application question using AI.
    """
    try:
        from backend.llm.gemini_service import get_gemini_service
        gemini = get_gemini_service()
        
        job_context = {
            "title": job_title,
            "company": company
        }
        
        answer = gemini.answer_application_question(
            question=question,
            job_context=job_context,
            resume_text=resume_text,
            max_words=max_words
        )
        
        return {
            "status": "success",
            "question": question,
            "answer": answer
        }
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(500, f"Failed to generate answer: {e}")


@router.get("/applications")
async def get_applications(
    user_email: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
):
    """
    Get application history.
    """
    # TODO: Implement database query
    # For now, return mock data
    
    return {
        "applications": [],
        "total": 0,
        "page": 1,
        "limit": limit
    }


@router.get("/jobs/search")
async def search_jobs(
    keywords: str,
    location: str = "Remote",
    max_results: int = 20
):
    """
    Search for jobs without automation (preview only).
    """
    try:
        from backend.automation.linkedin_scraper import search_linkedin_jobs
        
        jobs = search_linkedin_jobs(
            keywords=keywords,
            location=location,
            max_results=max_results
        )
        
        return {
            "jobs": jobs,
            "count": len(jobs)
        }
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(500, f"Job search failed: {e}")


# ==========================================
# Background Task Functions
# ==========================================

async def execute_agent_workflow(data: Dict[str, Any]):
    """
    Execute the complete agent workflow in the background.
    """
    import asyncio
    
    try:
        app_state.current_phase = "initializing"
        app_state.add_log("INFO", "Initializing automation")
        
        # Initialize orchestrator
        from backend.agents.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        
        # Prepare search criteria
        search_criteria = {
            "keywords": data.get("keywords", ""),
            "location": data.get("location", "Remote"),
            "linkedin_email": data.get("linkedin_email", ""),
            "linkedin_password": data.get("linkedin_password", ""),
            "submit": data.get("submit", False)
        }
        
        app_state.current_phase = "executing"
        app_state.add_log("INFO", f"Starting job search: {search_criteria['keywords']}")
        
        # Execute workflow
        result = await orchestrator.execute_job_search_workflow(
            user_id="default_user",
            search_criteria=search_criteria
        )
        
        # Update state
        app_state.jobs_found = result.get("jobs_found", 0)
        if search_criteria["submit"]:
            app_state.applications_submitted = result.get("applications_created", 0)
        else:
            app_state.applications_previewed = result.get("applications_created", 0)
        
        app_state.status = "completed"
        app_state.end_time = datetime.now()
        app_state.current_phase = "completed"
        app_state.add_log("INFO", "Workflow completed successfully")
        
    except Exception as e:
        logger.error(f"Agent workflow error: {e}")
        app_state.status = "failed"
        app_state.end_time = datetime.now()
        app_state.errors.append(str(e))
        app_state.add_log("ERROR", str(e))
