from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.services.application_service import ApplicationService

router = APIRouter()

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[ApplicationStatus] = None,
    db: Session = Depends(get_db)
):
    """Get user's job applications"""
    query = db.query(Application)
    
    if status_filter:
        query = query.filter(Application.status == status_filter)
    
    applications = query.offset(skip).limit(limit).all()
    return applications

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Submit a job application"""
    application_service = ApplicationService(db)
    db_application = await application_service.create_application(application)
    return db_application

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application by ID"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update application status or notes"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    for field, value in application_update.dict(exclude_unset=True).items():
        setattr(application, field, value)
    
    db.commit()
    db.refresh(application)
    return application

@router.post("/batch-apply")
async def batch_apply_jobs(
    job_ids: List[int],
    db: Session = Depends(get_db)
):
    """Apply to multiple jobs in batch using automation"""
    application_service = ApplicationService(db)
    results = await application_service.batch_apply(job_ids)
    return {"message": f"Applied to {len(results)} jobs", "results": results}