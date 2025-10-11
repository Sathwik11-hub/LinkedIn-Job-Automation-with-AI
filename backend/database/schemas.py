"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


# Resume Schemas
class ResumeUpload(BaseModel):
    """Schema for resume upload."""
    file_type: str
    file_path: str


class ResumeResponse(BaseModel):
    """Schema for resume response."""
    id: int
    user_id: int
    file_path: str
    file_type: str
    parsed_data: Optional[Dict[str, Any]] = None
    skills: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Schemas
class JobSearchRequest(BaseModel):
    """Schema for job search request."""
    keywords: str
    location: Optional[str] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    max_results: int = Field(default=50, le=100)


class JobListingResponse(BaseModel):
    """Schema for job listing response."""
    id: int
    title: str
    company: str
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    posted_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Application Schemas
class ApplicationCreate(BaseModel):
    """Schema for creating an application."""
    job_id: int
    cover_letter: Optional[str] = None
    custom_responses: Optional[Dict[str, Any]] = None


class ApplicationResponse(BaseModel):
    """Schema for application response."""
    id: int
    user_id: int
    job_id: int
    status: str
    cover_letter: Optional[str] = None
    applied_at: Optional[datetime] = None
    last_updated: datetime
    
    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    """Schema for updating application status."""
    status: str
    notes: Optional[str] = None


# Job Match Schemas
class JobMatchResponse(BaseModel):
    """Schema for job match response."""
    id: int
    job_id: int
    match_score: float
    reasoning: Optional[str] = None
    strengths: Optional[List[str]] = None
    gaps: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Preferences Schemas
class UserPreferences(BaseModel):
    """Schema for user job preferences."""
    desired_roles: List[str] = []
    desired_locations: List[str] = []
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    job_types: List[str] = []
    experience_levels: List[str] = []
    enable_auto_apply: bool = False
    max_applications_per_day: int = 10
    enable_email_notifications: bool = True


# Token Schemas
class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """Schema for token data."""
    email: Optional[str] = None
