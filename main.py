"""FastAPI backend for AutoAgentHire."""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from src.core import setup_logging, get_settings, get_logger
from src.models import (
    JobSearchFilters, SearchJobsResponse, MatchScoreResponse, 
    AutoApplyRequest, ApplicationRecord, ResumeData, JobPosting,
    JobMatch, CoverLetter
)
from src.services import (
    LinkedInScraper, ResumeParser, JobMatchingService,
    CoverLetterGenerator, ApplicationAutomator
)

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AutoAgentHire",
    description="AI-powered LinkedIn job automation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
resume_parser = ResumeParser()
job_matching_service = JobMatchingService()
cover_letter_generator = CoverLetterGenerator()

# Global storage for parsed resume
current_resume: Optional[ResumeData] = None
cached_jobs: List[JobPosting] = []


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting AutoAgentHire API")
    settings = get_settings()
    
    # Ensure data directories exist
    Path(settings.resume_path).mkdir(parents=True, exist_ok=True)
    Path(settings.jobs_data_path).mkdir(parents=True, exist_ok=True)
    Path(settings.logs_path).mkdir(parents=True, exist_ok=True)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down AutoAgentHire API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AutoAgentHire API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "resume_parser": "ready",
            "job_matching": "ready",
            "cover_letter_generator": "ready"
        }
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume PDF."""
    global current_resume
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Save uploaded file
        settings = get_settings()
        file_path = Path(settings.resume_path) / file.filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse resume
        logger.info(f"Parsing uploaded resume: {file.filename}")
        current_resume = resume_parser.parse_pdf(str(file_path))
        
        return {
            "message": "Resume uploaded and parsed successfully",
            "resume_data": current_resume.dict(),
            "filename": file.filename
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@app.get("/resume-status")
async def get_resume_status():
    """Get current resume status."""
    if current_resume:
        return {
            "status": "loaded",
            "resume_data": current_resume.dict()
        }
    else:
        return {
            "status": "no_resume",
            "message": "No resume has been uploaded"
        }


@app.post("/search-jobs", response_model=SearchJobsResponse)
async def search_jobs(filters: JobSearchFilters):
    """Search for jobs on LinkedIn."""
    global cached_jobs
    
    try:
        logger.info(f"Searching jobs with keywords: {filters.keywords}")
        
        async with LinkedInScraper() as scraper:
            # Login and search
            if not scraper.login():
                raise HTTPException(status_code=401, detail="Failed to login to LinkedIn")
            
            jobs = scraper.search_jobs(filters)
            cached_jobs = jobs
            
            # Add jobs to vector index for matching
            if jobs:
                job_matching_service.add_jobs_to_index(jobs)
            
            response = SearchJobsResponse(
                jobs=jobs,
                total_count=len(jobs),
                search_filters=filters
            )
            
            logger.info(f"Found {len(jobs)} jobs")
            return response
            
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")


@app.post("/match-jobs", response_model=MatchScoreResponse)
async def match_jobs(job_ids: Optional[List[str]] = None, top_k: int = 20):
    """Match jobs to uploaded resume."""
    if not current_resume:
        raise HTTPException(status_code=400, detail="No resume uploaded. Please upload a resume first.")
    
    try:
        logger.info(f"Matching jobs to resume (top_k={top_k})")
        
        # If specific job IDs provided, filter jobs
        jobs_to_match = cached_jobs
        if job_ids:
            jobs_to_match = [job for job in cached_jobs if job.job_id in job_ids]
            if not jobs_to_match:
                raise HTTPException(status_code=404, detail="No matching jobs found for provided IDs")
        
        # Ensure jobs are in the index
        if jobs_to_match:
            job_matching_service.add_jobs_to_index(jobs_to_match)
        
        # Perform matching
        matches = job_matching_service.match_jobs(current_resume, top_k)
        
        response = MatchScoreResponse(
            matches=matches,
            resume_summary=current_resume
        )
        
        logger.info(f"Generated {len(matches)} job matches")
        return response
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error matching jobs: {str(e)}")


@app.post("/generate-cover-letters")
async def generate_cover_letters(
    job_ids: List[str],
    custom_template: Optional[str] = None
) -> Dict[str, CoverLetter]:
    """Generate cover letters for specified jobs."""
    if not current_resume:
        raise HTTPException(status_code=400, detail="No resume uploaded. Please upload a resume first.")
    
    try:
        cover_letters = {}
        
        for job_id in job_ids:
            # Find job posting
            job = next((j for j in cached_jobs if j.job_id == job_id), None)
            if not job:
                logger.warning(f"Job {job_id} not found in cached jobs")
                continue
            
            # Generate cover letter
            logger.info(f"Generating cover letter for job: {job_id}")
            cover_letter = cover_letter_generator.generate_cover_letter(
                job, current_resume, custom_template
            )
            cover_letters[job_id] = cover_letter
        
        logger.info(f"Generated {len(cover_letters)} cover letters")
        return cover_letters
        
    except Exception as e:
        logger.error(f"Error generating cover letters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating cover letters: {str(e)}")


@app.post("/auto-apply")
async def auto_apply(request: AutoApplyRequest, background_tasks: BackgroundTasks):
    """Auto-apply to selected jobs."""
    if not current_resume:
        raise HTTPException(status_code=400, detail="No resume uploaded. Please upload a resume first.")
    
    try:
        # Filter jobs by similarity score if specified
        jobs_to_apply = []
        
        for job_id in request.job_ids:
            job = next((j for j in cached_jobs if j.job_id == job_id), None)
            if job:
                jobs_to_apply.append(job)
        
        if not jobs_to_apply:
            raise HTTPException(status_code=404, detail="No valid jobs found for application")
        
        # Generate cover letters
        logger.info(f"Generating cover letters for {len(jobs_to_apply)} jobs")
        cover_letters = {}
        
        for job in jobs_to_apply:
            cover_letter = cover_letter_generator.generate_cover_letter(
                job, current_resume, request.custom_cover_letter_template
            )
            cover_letters[job.job_id] = cover_letter
        
        # Start application process in background
        if request.dry_run:
            logger.info("Performing dry run - no actual applications will be submitted")
        
        background_tasks.add_task(
            apply_to_jobs_background,
            jobs_to_apply,
            cover_letters,
            request.dry_run
        )
        
        return {
            "message": f"Started application process for {len(jobs_to_apply)} jobs",
            "dry_run": request.dry_run,
            "job_count": len(jobs_to_apply)
        }
        
    except Exception as e:
        logger.error(f"Error starting auto-apply: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting auto-apply: {str(e)}")


async def apply_to_jobs_background(
    jobs: List[JobPosting],
    cover_letters: Dict[str, CoverLetter],
    dry_run: bool
):
    """Background task to apply to jobs."""
    try:
        async with ApplicationAutomator() as automator:
            records = automator.apply_to_jobs(jobs, cover_letters, dry_run)
            
            # Log results
            applied_count = sum(1 for r in records if r.status == "applied")
            skipped_count = sum(1 for r in records if r.status == "skipped")
            error_count = sum(1 for r in records if r.status == "error")
            
            logger.info(
                f"Application process completed: "
                f"{applied_count} applied, {skipped_count} skipped, {error_count} errors"
            )
            
    except Exception as e:
        logger.error(f"Background application process failed: {str(e)}")


@app.get("/application-status")
async def get_application_status():
    """Get status of recent applications."""
    # This would typically query a database
    # For now, return a placeholder response
    return {
        "message": "Application status tracking not yet implemented",
        "suggestion": "Check logs for application results"
    }


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    try:
        # Get vector database stats
        index_stats = job_matching_service.get_index_stats()
        
        return {
            "resume_loaded": current_resume is not None,
            "cached_jobs": len(cached_jobs),
            "vector_db_stats": index_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@app.delete("/clear-cache")
async def clear_cache():
    """Clear all cached data."""
    global current_resume, cached_jobs
    
    try:
        current_resume = None
        cached_jobs = []
        job_matching_service.clear_index()
        
        logger.info("Cache cleared successfully")
        return {"message": "Cache cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )