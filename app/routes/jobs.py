"""
Job search and application API routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel

from app.services.job_scraper import JobScraper
from app.services.matcher import JobMatcher
from app.services.auto_apply import AutoApply
from app.models.job_schema import Job, JobSearchRequest, ApplicationRequest
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


# Request/Response models
class JobSearchResponse(BaseModel):
    jobs: List[Job]
    total_count: int
    page: int
    per_page: int


class ApplicationResponse(BaseModel):
    success: bool
    message: str
    application_id: Optional[str] = None


@router.post("/jobs/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """
    Search for jobs on LinkedIn based on criteria
    """
    try:
        logger.info(f"Searching jobs with criteria: {request.dict()}")
        
        scraper = JobScraper()
        jobs = await scraper.search_jobs(
            keywords=request.keywords,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            limit=request.limit
        )
        
        return JobSearchResponse(
            jobs=jobs,
            total_count=len(jobs),
            page=1,
            per_page=request.limit
        )
        
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search jobs: {str(e)}")


@router.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """
    Get detailed information about a specific job
    """
    try:
        scraper = JobScraper()
        job = await scraper.get_job_details(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get job: {str(e)}")


@router.post("/jobs/match", response_model=List[Job])
async def match_jobs(request: JobSearchRequest):
    """
    Find and rank jobs based on resume matching
    """
    try:
        logger.info(f"Matching jobs for resume: {request.resume_path}")
        
        # First search for jobs
        scraper = JobScraper()
        jobs = await scraper.search_jobs(
            keywords=request.keywords,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level,
            limit=request.limit
        )
        
        # Then match and rank them
        matcher = JobMatcher()
        matched_jobs = await matcher.match_jobs(jobs, request.resume_path)
        
        return matched_jobs
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to match jobs: {str(e)}")


@router.post("/jobs/apply", response_model=ApplicationResponse)
async def apply_to_job(request: ApplicationRequest, background_tasks: BackgroundTasks):
    """
    Apply to a specific job with auto-generated cover letter
    """
    try:
        logger.info(f"Applying to job {request.job_id}")
        
        auto_apply = AutoApply()
        
        # Add application task to background
        background_tasks.add_task(
            auto_apply.apply_to_job,
            request.job_id,
            request.resume_path,
            request.cover_letter_template
        )
        
        return ApplicationResponse(
            success=True,
            message="Application submitted successfully",
            application_id=f"app_{request.job_id}_{int(__import__('time').time())}"
        )
        
    except Exception as e:
        logger.error(f"Error applying to job {request.job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to apply to job: {str(e)}")


@router.post("/jobs/bulk-apply")
async def bulk_apply_jobs(
    job_ids: List[str],
    resume_path: str,
    background_tasks: BackgroundTasks
):
    """
    Apply to multiple jobs in bulk
    """
    try:
        logger.info(f"Bulk applying to {len(job_ids)} jobs")
        
        auto_apply = AutoApply()
        
        # Add bulk application task to background
        background_tasks.add_task(
            auto_apply.bulk_apply,
            job_ids,
            resume_path
        )
        
        return {
            "success": True,
            "message": f"Bulk application started for {len(job_ids)} jobs",
            "job_count": len(job_ids)
        }
        
    except Exception as e:
        logger.error(f"Error in bulk apply: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start bulk application: {str(e)}")


@router.get("/jobs/applications/status")
async def get_application_status():
    """
    Get status of ongoing applications
    """
    try:
        auto_apply = AutoApply()
        status = await auto_apply.get_application_status()
        
        return status
        
    except Exception as e:
        logger.error(f"Error getting application status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get application status: {str(e)}")