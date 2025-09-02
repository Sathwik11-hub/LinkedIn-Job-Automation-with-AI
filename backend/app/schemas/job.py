from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None

class JobCreate(JobBase):
    linkedin_job_id: Optional[str] = None
    job_url: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    company_size: Optional[str] = None
    industry: Optional[str] = None
    skills_required: Optional[str] = None
    remote_option: bool = False
    posted_date: Optional[datetime] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class JobResponse(JobBase):
    id: int
    linkedin_job_id: Optional[str]
    job_url: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    company_size: Optional[str]
    industry: Optional[str]
    skills_required: Optional[str]
    remote_option: bool
    posted_date: Optional[datetime]
    scraped_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class JobSearchParams(BaseModel):
    keywords: str
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    remote_option: Optional[bool] = None
    salary_min: Optional[float] = None
    company_size: Optional[str] = None
    date_posted: Optional[str] = None  # "24h", "week", "month"
    
    @validator('keywords')
    def validate_keywords(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Keywords must be at least 2 characters long')
        return v.strip()