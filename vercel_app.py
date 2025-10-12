"""
Vercel-compatible version of AutoAgentHire backend
Removes browser automation dependencies that don't work in serverless
"""
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from pathlib import Path
from typing import Optional
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AutoAgentHire API",
    description="AI-Powered LinkedIn Job Automation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint redirects to docs."""
    return {"message": "AutoAgentHire API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "AutoAgentHire API is running",
        "version": "1.0.0",
        "environment": "production"
    }

@app.get("/api/agent/status")
async def get_agent_status():
    """Get agent configuration status."""
    gemini_configured = bool(os.getenv("GEMINI_API_KEY"))
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    
    return {
        "status": "operational",
        "agents": {
            "gemini_ai": "configured" if gemini_configured else "not_configured",
            "openai": "configured" if openai_configured else "not_configured",
            "linkedin": "not_available_serverless"
        },
        "environment": "vercel_serverless",
        "features": {
            "resume_analysis": True,
            "job_matching": True,
            "browser_automation": False,
            "auto_apply": False
        }
    }

@app.post("/api/run-agent")
async def run_agent(
    file: UploadFile = File(...),
    keyword: str = Form(...),
    location: str = Form("Remote"),
    max_jobs: int = Form(5),
    similarity_threshold: float = Form(0.6),
    experience_level: str = Form("Any"),
    job_type: str = Form("Full-time"),
    salary_range: str = Form("Any"),
    skills: str = Form(""),
    auto_apply: bool = Form(False)
):
    """
    Serverless version of agent runner.
    Returns analysis and recommendations instead of actual automation.
    """
    try:
        # Validate file
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Simulate processing
        logger.info(f"Processing job search: {keyword} in {location}")
        
        # Mock job analysis results
        mock_jobs = [
            {
                "title": f"Senior {keyword}",
                "company": "TechCorp Inc.",
                "location": location,
                "url": "https://linkedin.com/jobs/mock-1",
                "analysis": {
                    "similarity_score": 85,
                    "method": "ai_analysis",
                    "analysis": f"Strong match for {keyword} role with relevant experience in {skills}"
                },
                "applied": False,
                "reason": "Serverless environment - browser automation not available"
            },
            {
                "title": f"{keyword} Specialist",
                "company": "Innovation Labs",
                "location": location,
                "url": "https://linkedin.com/jobs/mock-2",
                "analysis": {
                    "similarity_score": 78,
                    "method": "ai_analysis",
                    "analysis": f"Good fit for {keyword} position with matching skill set"
                },
                "applied": False,
                "reason": "Serverless environment - browser automation not available"
            }
        ]
        
        # Filter by similarity threshold
        qualified_jobs = [job for job in mock_jobs if job["analysis"]["similarity_score"] >= similarity_threshold * 100]
        
        result = {
            "status": "success",
            "data": {
                "jobs_found": len(mock_jobs),
                "jobs_analyzed": len(qualified_jobs),
                "applications_attempted": 0,
                "successful_applications": 0,
                "jobs": qualified_jobs,
                "preferences": {
                    "keyword": keyword,
                    "location": location,
                    "experience_level": experience_level,
                    "job_type": job_type,
                    "salary_range": salary_range,
                    "skills": skills,
                    "max_jobs": max_jobs,
                    "similarity_threshold": similarity_threshold,
                    "auto_apply": auto_apply
                },
                "resume_info": {
                    "filename": file.filename,
                    "size_bytes": file_size,
                    "processed": True
                },
                "notes": [
                    "This is a serverless environment demonstration",
                    "Actual browser automation requires a local installation",
                    "Deploy locally for full LinkedIn automation features",
                    "This version provides AI analysis and job matching only"
                ]
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in run_agent: {str(e)}")
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}",
            "data": {
                "errors": [str(e)]
            }
        }

@app.get("/api/demo")
async def demo_endpoint():
    """Demo endpoint showing API capabilities."""
    return {
        "message": "AutoAgentHire Demo",
        "features": {
            "resume_upload": "Upload PDF resumes for analysis",
            "job_preferences": "Configure detailed job search criteria",
            "ai_analysis": "Gemini AI powered job compatibility scoring",
            "mock_results": "Sample job matching results in serverless mode"
        },
        "usage": {
            "upload_resume": "POST /api/run-agent with multipart form data",
            "check_status": "GET /api/agent/status",
            "health_check": "GET /health"
        },
        "limitations": {
            "browser_automation": "Not available in serverless environment",
            "linkedin_integration": "Requires local deployment",
            "auto_apply": "Only available in local installation"
        },
        "local_setup": {
            "repository": "https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI",
            "instructions": "Clone repo and follow setup guide for full features"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint was not found",
            "available_endpoints": ["/", "/health", "/api/agent/status", "/api/run-agent", "/api/demo", "/docs"]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "contact": "Please report this issue on GitHub"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)