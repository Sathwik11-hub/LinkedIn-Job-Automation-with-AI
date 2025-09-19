from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from app.core.database import get_db
from app.models.application import Application, ApplicationStatus
from app.models.job import Job
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get dashboard statistics for user"""
    
    # Application statistics
    total_applications = db.query(Application).count()
    pending_applications = db.query(Application).filter(
        Application.status == ApplicationStatus.PENDING
    ).count()
    successful_applications = db.query(Application).filter(
        Application.status.in_([
            ApplicationStatus.INTERVIEW_REQUESTED,
            ApplicationStatus.INTERVIEW_SCHEDULED,
            ApplicationStatus.OFFER_RECEIVED
        ])
    ).count()
    
    # Success rate
    success_rate = (successful_applications / total_applications * 100) if total_applications > 0 else 0
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_applications = db.query(Application).filter(
        Application.application_date >= thirty_days_ago
    ).count()
    
    # Jobs by status
    status_breakdown = db.query(
        Application.status,
        func.count(Application.id).label('count')
    ).group_by(Application.status).all()
    
    status_dict = {status.value: 0 for status in ApplicationStatus}
    for status, count in status_breakdown:
        status_dict[status.value] = count
    
    return {
        "total_applications": total_applications,
        "pending_applications": pending_applications,
        "successful_applications": successful_applications,
        "success_rate": round(success_rate, 2),
        "recent_applications": recent_applications,
        "status_breakdown": status_dict
    }

@router.get("/analytics")
async def get_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed analytics for specified time period"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Applications over time
    applications_by_date = db.query(
        func.date(Application.application_date).label('date'),
        func.count(Application.id).label('count')
    ).filter(
        Application.application_date >= start_date
    ).group_by(func.date(Application.application_date)).all()
    
    # Top companies applied to
    top_companies = db.query(
        Job.company,
        func.count(Application.id).label('application_count')
    ).join(Application).filter(
        Application.application_date >= start_date
    ).group_by(Job.company).order_by(
        func.count(Application.id).desc()
    ).limit(10).all()
    
    # Job types applied to
    job_types = db.query(
        Job.job_type,
        func.count(Application.id).label('count')
    ).join(Application).filter(
        Application.application_date >= start_date
    ).group_by(Job.job_type).all()
    
    return {
        "period_days": days,
        "applications_by_date": [
            {"date": str(date), "count": count} 
            for date, count in applications_by_date
        ],
        "top_companies": [
            {"company": company, "applications": count}
            for company, count in top_companies
        ],
        "job_types": [
            {"type": job_type, "count": count}
            for job_type, count in job_types
        ]
    }