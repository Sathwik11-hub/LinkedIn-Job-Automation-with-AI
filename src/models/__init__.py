"""Data models for AutoAgentHire application."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class JobExperienceLevel(str, Enum):
    """Job experience levels."""
    INTERNSHIP = "Internship"
    ENTRY_LEVEL = "Entry level"
    ASSOCIATE = "Associate"
    MID_SENIOR = "Mid-Senior level"
    DIRECTOR = "Director"
    EXECUTIVE = "Executive"


class ApplicationStatus(str, Enum):
    """Application status enum."""
    PENDING = "pending"
    APPLIED = "applied"
    REJECTED = "rejected"
    INTERVIEW = "interview"
    OFFER = "offer"
    SKIPPED = "skipped"
    ERROR = "error"


class JobPosting(BaseModel):
    """Job posting model."""
    job_id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    description: str = Field(..., description="Job description")
    requirements: Optional[str] = Field(None, description="Job requirements")
    experience_level: Optional[JobExperienceLevel] = Field(None, description="Required experience level")
    salary_range: Optional[str] = Field(None, description="Salary range")
    job_type: Optional[str] = Field(None, description="Job type (Full-time, Part-time, etc.)")
    url: str = Field(..., description="Job posting URL")
    posted_date: Optional[datetime] = Field(None, description="Date when job was posted")
    scraped_at: datetime = Field(default_factory=datetime.now, description="When the job was scraped")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ResumeData(BaseModel):
    """Resume data model."""
    file_path: str = Field(..., description="Path to resume file")
    name: Optional[str] = Field(None, description="Candidate name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    skills: List[str] = Field(default_factory=list, description="List of skills")
    experience: List[Dict[str, Any]] = Field(default_factory=list, description="Work experience")
    education: List[Dict[str, Any]] = Field(default_factory=list, description="Education background")
    summary: Optional[str] = Field(None, description="Professional summary")
    parsed_at: datetime = Field(default_factory=datetime.now, description="When resume was parsed")


class JobMatch(BaseModel):
    """Job matching result model."""
    job_id: str = Field(..., description="Job identifier")
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score between 0 and 1")
    matched_skills: List[str] = Field(default_factory=list, description="Skills that matched")
    missing_skills: List[str] = Field(default_factory=list, description="Skills that were missing")
    recommendation: str = Field(..., description="Apply recommendation")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the match")


class CoverLetter(BaseModel):
    """Cover letter model."""
    job_id: str = Field(..., description="Associated job ID")
    content: str = Field(..., description="Cover letter content")
    personalization_score: float = Field(..., ge=0.0, le=1.0, description="How personalized the letter is")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")


class ApplicationRecord(BaseModel):
    """Application record model."""
    id: Optional[str] = Field(None, description="Application record ID")
    job_id: str = Field(..., description="Job identifier")
    job_title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    applied_at: datetime = Field(default_factory=datetime.now, description="Application timestamp")
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING, description="Application status")
    cover_letter_id: Optional[str] = Field(None, description="Associated cover letter ID")
    similarity_score: Optional[float] = Field(None, description="Job match score")
    notes: Optional[str] = Field(None, description="Additional notes")
    error_message: Optional[str] = Field(None, description="Error message if application failed")


class JobSearchFilters(BaseModel):
    """Job search filters model."""
    keywords: str = Field(..., description="Search keywords")
    location: str = Field(default="Remote", description="Job location")
    experience_level: Optional[JobExperienceLevel] = Field(None, description="Experience level filter")
    job_type: Optional[str] = Field(None, description="Job type filter")
    date_posted: Optional[str] = Field(None, description="Date posted filter")
    company_size: Optional[str] = Field(None, description="Company size filter")
    industry: Optional[str] = Field(None, description="Industry filter")
    salary_range: Optional[str] = Field(None, description="Salary range filter")
    remote_only: bool = Field(default=False, description="Remote jobs only")
    max_results: int = Field(default=50, ge=1, le=1000, description="Maximum number of results")


class AutoApplyRequest(BaseModel):
    """Auto-apply request model."""
    job_ids: List[str] = Field(..., description="List of job IDs to apply to")
    min_similarity_score: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum similarity score")
    custom_cover_letter_template: Optional[str] = Field(None, description="Custom cover letter template")
    dry_run: bool = Field(default=True, description="Whether to do a dry run without actually applying")


class SearchJobsResponse(BaseModel):
    """Search jobs response model."""
    jobs: List[JobPosting] = Field(..., description="List of found jobs")
    total_count: int = Field(..., description="Total number of jobs found")
    search_filters: JobSearchFilters = Field(..., description="Filters used for search")
    search_time: datetime = Field(default_factory=datetime.now, description="Search timestamp")


class MatchScoreResponse(BaseModel):
    """Match and score response model."""
    matches: List[JobMatch] = Field(..., description="List of job matches")
    resume_summary: ResumeData = Field(..., description="Resume data used for matching")
    processed_at: datetime = Field(default_factory=datetime.now, description="Processing timestamp")