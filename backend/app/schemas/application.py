from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus

class ApplicationBase(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    user_id: int
    custom_resume_path: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None
    response_received: Optional[bool] = None

class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: ApplicationStatus
    application_date: datetime
    last_updated: datetime
    custom_resume_path: Optional[str]
    interview_date: Optional[datetime]
    response_received: bool
    automated: bool
    success_score: Optional[int]
    
    class Config:
        from_attributes = True

class ApplicationStats(BaseModel):
    total_applications: int
    pending_applications: int
    successful_applications: int
    success_rate: float
    recent_applications: int