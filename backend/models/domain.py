"""
Data models for business logic (separate from database models).

These are domain models used throughout the application logic,
independent of the database layer.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, validator


class JobStatus(str, Enum):
    """Enum for job posting status."""
    
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    ARCHIVED = "archived"


class ApplicationStatus(str, Enum):
    """Enum for application status."""
    
    PENDING = "pending"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW = "interview"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Job(BaseModel):
    """Domain model for a job posting."""
    
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: List[str] = Field(default_factory=list)
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    employment_type: str = "full_time"
    experience_level: str = "mid"
    posted_date: datetime
    status: JobStatus = JobStatus.ACTIVE
    url: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class Resume(BaseModel):
    """Domain model for a resume."""
    
    id: str
    user_id: str
    file_path: str
    parsed_data: Dict[str, Any] = Field(default_factory=dict)
    skills: List[str] = Field(default_factory=list)
    experience_years: float = 0.0
    education: List[Dict[str, str]] = Field(default_factory=list)
    work_history: List[Dict[str, Any]] = Field(default_factory=list)
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Application(BaseModel):
    """Domain model for a job application."""
    
    id: str
    job_id: str
    user_id: str
    resume_id: str
    cover_letter: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.PENDING
    match_score: float = 0.0
    applied_date: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    
    class Config:
        use_enum_values = True


class User(BaseModel):
    """Domain model for a user."""
    
    id: str
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class JobSearchQuery(BaseModel):
    """Domain model for job search parameters."""
    
    keywords: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    remote: bool = False
    salary_min: Optional[float] = None
    experience_level: Optional[str] = None
    employment_type: Optional[str] = None
    company: Optional[str] = None
    posted_within_days: int = 30
    
    @validator('keywords')
    def keywords_not_empty(cls, v):
        """Validate that keywords list is not empty."""
        if not v:
            raise ValueError('At least one keyword is required')
        return v


class JobMatch(BaseModel):
    """Domain model for job matching results."""
    
    job: Job
    match_score: float = Field(ge=0.0, le=1.0)
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)


class AgentTask(BaseModel):
    """Domain model for agent tasks."""
    
    id: str
    agent_type: str
    task_type: str
    status: str = "pending"
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Notification(BaseModel):
    """Domain model for notifications."""
    
    id: str
    user_id: str
    title: str
    message: str
    notification_type: str = "info"
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    data: Optional[Dict[str, Any]] = None


class CoverLetter(BaseModel):
    """Domain model for cover letters."""
    
    id: str
    application_id: str
    user_id: str
    job_id: str
    content: str
    generated_by: str = "ai"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_customized: bool = False


class WorkflowExecution(BaseModel):
    """Domain model for workflow execution tracking."""
    
    id: str
    workflow_type: str
    status: str = "running"
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    current_step: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
