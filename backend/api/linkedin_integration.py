"""
FastAPI Integration for LinkedIn Auto Apply
Connects the Playwright automation with the existing FastAPI backend
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio
import logging
from datetime import datetime

from linkedin_auto_apply import LinkedInAutoApply, JobListing, ApplicationResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/linkedin", tags=["LinkedIn Automation"])

# In-memory state (replace with Redis or DB in production)
automation_state = {
    "status": "idle",  # idle, running, completed, failed
    "current_job": None,
    "total_jobs": 0,
    "jobs_analyzed": 0,
    "applications_submitted": 0,
    "start_time": None,
    "error": None
}


class LinkedInAutoApplyRequest(BaseModel):
    """Request model for LinkedIn auto-apply."""
    linkedin_email: str = Field(..., description="LinkedIn email address")
    linkedin_password: str = Field(..., description="LinkedIn password")
    resume_path: str = Field(..., description="Path to resume file")
    
    # Search criteria
    keywords: str = Field(..., description="Job search keywords", example="AI Engineer")
    location: str = Field(default="United States", description="Job location")
    experience_level: Optional[str] = Field(None, description="Experience level filter")
    job_type: Optional[str] = Field(None, description="Job type filter")
    
    # Configuration
    max_jobs: int = Field(default=50, ge=1, le=100, description="Maximum jobs to parse")
    max_applications: int = Field(default=5, ge=1, le=10, description="Maximum applications to submit")
    match_threshold: float = Field(default=75.0, ge=0, le=100, description="Match threshold percentage")
    
    # Options
    headless: bool = Field(default=True, description="Run browser in headless mode")
    use_llm: bool = Field(default=True, description="Use LLM for cover letter generation")
    send_email_report: bool = Field(default=False, description="Send email report after completion")


class LinkedInStatusResponse(BaseModel):
    """Response model for automation status."""
    status: str
    current_job: Optional[str]
    total_jobs: int
    jobs_analyzed: int
    applications_submitted: int
    start_time: Optional[str]
    error: Optional[str]


class LinkedInReportResponse(BaseModel):
    """Response model for automation report."""
    session_date: str
    statistics: dict
    top_matches: List[dict]
    applications: List[dict]


async def run_automation_background(request: LinkedInAutoApplyRequest):
    """
    Run LinkedIn automation in background.
    
    This function is called as a background task to avoid blocking the API.
    """
    global automation_state
    
    try:
        # Update state
        automation_state["status"] = "running"
        automation_state["start_time"] = datetime.now().isoformat()
        automation_state["error"] = None
        
        logger.info(f"🚀 Starting LinkedIn automation for {request.keywords}")
        
        # Create automation agent
        agent = LinkedInAutoApply(
            email=request.linkedin_email,
            password=request.linkedin_password,
            resume_path=request.resume_path,
            headless=request.headless,
            use_llm=request.use_llm
        )
        
        # Override configuration
        agent.max_applications_per_session = request.max_applications
        agent.match_threshold = request.match_threshold
        
        # Run automation with state updates
        await agent.initialize_browser()
        automation_state["status"] = "logging_in"
        
        login_success = await agent.login_linkedin()
        if not login_success:
            raise Exception("LinkedIn login failed")
        
        automation_state["status"] = "searching"
        jobs_count = await agent.search_jobs(
            keywords=request.keywords,
            location=request.location,
            experience_level=request.experience_level,
            job_type=request.job_type,
            easy_apply_only=True
        )
        
        automation_state["total_jobs"] = jobs_count
        automation_state["status"] = "parsing"
        
        await agent.parse_job_listings(max_jobs=request.max_jobs)
        
        automation_state["status"] = "analyzing"
        await agent.analyze_all_jobs()
        automation_state["jobs_analyzed"] = len(agent.jobs_found)
        
        automation_state["status"] = "applying"
        
        # Apply to jobs with progress updates
        qualified_jobs = [j for j in agent.jobs_found if j.match_score >= request.match_threshold]
        jobs_to_apply = qualified_jobs[:request.max_applications]
        
        for i, job in enumerate(jobs_to_apply, 1):
            automation_state["current_job"] = f"{job.title} at {job.company}"
            
            result = await agent.auto_apply_job(job)
            agent.jobs_applied.append(result)
            
            if result.status == 'success':
                automation_state["applications_submitted"] += 1
            
            # Delay between applications
            if i < len(jobs_to_apply):
                await asyncio.sleep(15)
        
        automation_state["status"] = "reporting"
        
        # Generate report
        report = agent.generate_report()
        agent.print_console_report(report)
        
        # Send email if requested
        if request.send_email_report:
            await agent.send_email_report(report)
        
        # Cleanup
        await agent.cleanup()
        
        automation_state["status"] = "completed"
        automation_state["current_job"] = None
        
        logger.info("✅ LinkedIn automation completed successfully")
    
    except Exception as e:
        logger.error(f"❌ LinkedIn automation failed: {e}")
        automation_state["status"] = "failed"
        automation_state["error"] = str(e)
        automation_state["current_job"] = None


@router.post("/auto-apply", response_model=dict)
async def start_auto_apply(
    request: LinkedInAutoApplyRequest,
    background_tasks: BackgroundTasks
):
    """
    Start LinkedIn auto-apply automation.
    
    This endpoint starts the automation in the background and returns immediately.
    Use the /status endpoint to check progress.
    """
    # Check if already running
    if automation_state["status"] == "running":
        raise HTTPException(
            status_code=409,
            detail="Automation is already running. Please wait for completion."
        )
    
    # Reset state
    automation_state.update({
        "status": "starting",
        "current_job": None,
        "total_jobs": 0,
        "jobs_analyzed": 0,
        "applications_submitted": 0,
        "start_time": None,
        "error": None
    })
    
    # Start automation in background
    background_tasks.add_task(run_automation_background, request)
    
    return {
        "status": "started",
        "message": "LinkedIn auto-apply automation started in background",
        "check_status_at": "/api/linkedin/status"
    }


@router.get("/status", response_model=LinkedInStatusResponse)
async def get_automation_status():
    """
    Get current automation status.
    
    Returns real-time status of the automation including:
    - Current status (idle, running, completed, failed)
    - Current job being processed
    - Total jobs found
    - Jobs analyzed
    - Applications submitted
    - Start time
    - Error message (if failed)
    """
    return LinkedInStatusResponse(**automation_state)


@router.post("/stop")
async def stop_automation():
    """
    Stop running automation.
    
    Note: This is a graceful stop. Current application will complete
    before stopping.
    """
    if automation_state["status"] != "running":
        raise HTTPException(
            status_code=400,
            detail="No automation is currently running"
        )
    
    automation_state["status"] = "stopping"
    
    return {
        "status": "stopping",
        "message": "Automation will stop after current application completes"
    }


@router.get("/reports/latest", response_model=dict)
async def get_latest_report():
    """
    Get the latest automation report.
    
    Returns the most recent report file generated by the automation.
    """
    import json
    from pathlib import Path
    
    reports_dir = Path("reports")
    if not reports_dir.exists():
        raise HTTPException(status_code=404, detail="No reports found")
    
    # Find latest report
    report_files = sorted(reports_dir.glob("session_*.json"), reverse=True)
    
    if not report_files:
        raise HTTPException(status_code=404, detail="No reports found")
    
    latest_report = report_files[0]
    
    with open(latest_report) as f:
        report = json.load(f)
    
    return report


@router.get("/reports", response_model=List[dict])
async def list_reports(limit: int = 10):
    """
    List all automation reports.
    
    Args:
        limit: Maximum number of reports to return (default: 10)
    """
    import json
    from pathlib import Path
    
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return []
    
    report_files = sorted(reports_dir.glob("session_*.json"), reverse=True)[:limit]
    
    reports = []
    for report_file in report_files:
        with open(report_file) as f:
            report = json.load(f)
            reports.append({
                "filename": report_file.name,
                "date": report["session_date"],
                "statistics": report["statistics"]
            })
    
    return reports


@router.delete("/reports/{filename}")
async def delete_report(filename: str):
    """Delete a specific report."""
    from pathlib import Path
    
    report_path = Path(f"reports/{filename}")
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not filename.startswith("session_") or not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Invalid report filename")
    
    report_path.unlink()
    
    return {"status": "deleted", "filename": filename}


@router.get("/test-connection")
async def test_linkedin_connection(
    email: str,
    password: str,
    headless: bool = False
):
    """
    Test LinkedIn connection without running full automation.
    
    This is useful for verifying credentials before starting automation.
    """
    try:
        agent = LinkedInAutoApply(
            email=email,
            password=password,
            resume_path="./data/resumes/dummy.txt",
            headless=headless,
            use_llm=False
        )
        
        await agent.initialize_browser()
        login_success = await agent.login_linkedin()
        await agent.cleanup()
        
        if login_success:
            return {
                "status": "success",
                "message": "LinkedIn connection successful"
            }
        else:
            return {
                "status": "failed",
                "message": "LinkedIn login failed. Please check credentials."
            }
    
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Connection test failed: {str(e)}"
        )


# Integration with existing backend
def register_linkedin_routes(app):
    """
    Register LinkedIn automation routes with FastAPI app.
    
    Usage:
        from backend.main import app
        from linkedin_integration import register_linkedin_routes
        
        register_linkedin_routes(app)
    """
    app.include_router(router)
    logger.info("✅ LinkedIn automation routes registered")
