"""
Pydantic models for job data
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class ExperienceLevel(str, Enum):
    ENTRY = "entry_level"
    ASSOCIATE = "associate"
    MID_SENIOR = "mid_senior_level"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


class JobSearchRequest(BaseModel):
    """Job search request model"""
    keywords: str = Field(..., description="Job search keywords")
    location: Optional[str] = Field("United States", description="Job location")
    job_type: Optional[str] = Field(None, description="Job type (full_time, part_time, etc.)")
    experience_level: Optional[str] = Field(None, description="Experience level")
    date_posted: Optional[str] = Field(None, description="Date posted (e.g. past_24_hours)")
    remote_filter: Optional[bool] = Field(False, description="Filter for remote jobs")
    limit: Optional[int] = Field(20, description="Maximum number of jobs to return")


class Job(BaseModel):
    """Job model"""
    job_id: str = Field(..., description="LinkedIn job ID")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    date_posted: Optional[str] = Field(None, description="Date when job was posted")
    description: Optional[str] = Field(None, description="Job description")
    url: str = Field(..., description="Job URL")
    is_remote: Optional[bool] = Field(False, description="Whether job is remote")
    salary_range: Optional[str] = Field(None, description="Salary range if available")
    requirements: Optional[List[str]] = Field(None, description="Job requirements")
    benefits: Optional[List[str]] = Field(None, description="Job benefits")
    match_score: Optional[float] = Field(None, description="Match score between 0 and 1")
    match_reasons: Optional[List[str]] = Field(None, description="Reasons for match score")


class JobMatchRequest(BaseModel):
    """Job match request model"""
    resume_path: str = Field(..., description="Path to resume file")
    keywords: Optional[str] = Field(None, description="Job search keywords")
    location: Optional[str] = Field("United States", description="Job location")
    include_match_score: Optional[bool] = Field(True, description="Include match score in results")
    limit: Optional[int] = Field(20, description="Maximum number of jobs to return")


class JobApplicationRequest(BaseModel):
    """Job application request model"""
    job_id: str = Field(..., description="LinkedIn job ID")
    resume_path: str = Field(..., description="Path to resume file")
    cover_letter_template: Optional[str] = Field("standard", description="Cover letter template type")


class Resume(BaseModel):
    """Resume model for parsing and analysis"""
    file_path: str = Field(..., description="Path to resume file")
    content: str = Field(..., description="Extracted text content")
    skills: List[str] = Field(default=[], description="Extracted skills")
    experience: List[str] = Field(default=[], description="Work experience")
    education: List[str] = Field(default=[], description="Education background")
    contact_info: Optional[dict] = Field(None, description="Contact information")
    summary: Optional[str] = Field(None, description="Professional summary")


class CoverLetter(BaseModel):
    """Cover letter model"""
    content: str = Field(..., description="Cover letter content")
    job_title: str = Field(..., description="Target job title")
    company_name: str = Field(..., description="Target company name")
    template_used: str = Field(..., description="Template used for generation")
    personalization_score: Optional[float] = Field(None, description="Personalization quality score")


class ApplicationStatus(BaseModel):
    """Application status tracking model"""
    application_id: str = Field(..., description="Unique application identifier")
    job_id: str = Field(..., description="Job ID")
    status: str = Field(..., description="Application status (pending, applied, rejected, etc.)")
    applied_date: str = Field(..., description="Date when application was submitted")
    response_date: Optional[str] = Field(None, description="Date of response if any")
    notes: Optional[str] = Field(None, description="Additional notes")


class ApplicationTracker(BaseModel):
    """Application tracking model for monitoring job applications"""
    application_id: str = Field(..., description="Unique application identifier")
    job: Job = Field(..., description="Job information")
    status: str = Field(default="pending", description="Current application status")
    applied_date: str = Field(..., description="Date when application was submitted")
    cover_letter_path: Optional[str] = Field(None, description="Path to generated cover letter")
    success: bool = Field(default=False, description="Whether application was successful")
    error_message: Optional[str] = Field(None, description="Error message if application failed")
    retry_count: int = Field(default=0, description="Number of retry attempts")
    custom_note: Optional[str] = Field(None, description="Custom note for cover letter")