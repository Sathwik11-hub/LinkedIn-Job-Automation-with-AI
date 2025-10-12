"""
FastAPI routes for AutoAgentHire automation.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import tempfile
import os
import logging
from typing import Optional

from backend.agents.auto_apply_agent_clean import run_autoagent

# Setup router
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/api/run-agent")
async def run_agent(
    file: UploadFile = File(...),
    keyword: str = Form("AI Engineer"),
    location: str = Form("India"),
    max_jobs: int = Form(10),
    similarity_threshold: float = Form(0.5),
    experience_level: str = Form("Any"),
    job_type: str = Form("Any"),
    salary_range: str = Form("Any"),
    skills: str = Form(""),
    auto_apply: bool = Form(True)
):
    """
    Run AutoAgent LinkedIn automation with resume upload.
    
    This endpoint:
    1. Accepts a resume PDF file upload
    2. Extracts text from the resume
    3. Opens Chromium browser (non-headless for visibility)
    4. Logs into LinkedIn using stored credentials
    5. Searches for jobs based on keyword and location
    6. Uses AI to analyze job compatibility
    7. Auto-applies to matching jobs
    8. Returns detailed results
    """
    temp_file_path = None
    
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported for resume upload"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"🚀 Starting AutoAgent for keyword: '{keyword}' in location: '{location}'")
        logger.info(f"📄 Resume uploaded: {file.filename} ({len(content)} bytes)")
        logger.info(f"🎯 Preferences: Experience={experience_level}, Type={job_type}, Auto-apply={auto_apply}")
        
        # Run the automation with enhanced preferences
        results = await run_autoagent(
            keyword=keyword,
            location=location,
            resume_path=temp_file_path,
            max_jobs=max_jobs,
            similarity_threshold=similarity_threshold,
            experience_level=experience_level,
            job_type=job_type,
            salary_range=salary_range,
            skills=skills,
            auto_apply=auto_apply
        )
        
        # Check for errors in results
        if isinstance(results, dict) and "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "AutoAgent automation completed successfully",
                "data": results
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error(f"❌ Run Agent error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Automation failed: {str(e)}"
        )
        
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.get("/api/agent/status")
async def get_agent_status():
    """Get the current status of automation components."""
    return {
        "status": "operational",
        "components": {
            "chromium_browser": "available",
            "linkedin_credentials": "configured" if os.getenv("LINKEDIN_EMAIL") else "not_configured",
            "gemini_ai": "configured" if os.getenv("GEMINI_API_KEY") else "not_configured",
            "playwright": "installed"
        },
        "features": [
            "Resume PDF processing",
            "LinkedIn job search",
            "AI-powered job matching",
            "Automated job applications",
            "Real browser automation (non-headless)"
        ]
    }


@router.post("/api/test-browser")
async def test_browser_initialization():
    """Test browser initialization without full automation."""
    try:
        return {"status": "success", "message": "Browser test endpoint available"}
    except Exception as e:
        logger.error(f"Browser test failed: {str(e)}")
        return {"status": "error", "message": str(e)}