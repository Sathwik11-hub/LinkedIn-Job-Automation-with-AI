from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobSearchParams
from app.services.job_service import JobService

router = APIRouter()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    remote_option: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get jobs with optional filtering"""
    query = db.query(Job)
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if job_type:
        query = query.filter(Job.job_type == job_type)
    if remote_option is not None:
        query = query.filter(Job.remote_option == remote_option)
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs

@router.post("/search", response_model=List[JobResponse])
async def search_jobs(
    search_params: JobSearchParams,
    db: Session = Depends(get_db)
):
    """Search for jobs based on criteria"""
    job_service = JobService(db)
    jobs = await job_service.search_jobs(search_params)
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job by ID"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting (admin only)"""
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job