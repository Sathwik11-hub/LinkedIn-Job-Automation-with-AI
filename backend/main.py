"""
Main FastAPI application entry point.
Initializes the application, middleware, and routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

from backend.config import settings
# from backend.api import routes
# from backend.utils.logger import setup_logger

# Setup logger
# logger = setup_logger(__name__)
import logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME}...")
    print(f"📝 Environment: {settings.APP_ENV}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    
    # TODO: Initialize database connection
    # TODO: Initialize vector store
    # TODO: Start background scheduler
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    # TODO: Close database connections
    # TODO: Clean up resources


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous AI agent system for job discovery and applications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip Middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "name": settings.APP_NAME,
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Check actual DB connection
        "vector_db": "connected",  # TODO: Check vector DB connection
    }


@app.post("/agents/job-search")
async def trigger_job_search_agent(request_data: dict):
    """Trigger the job search agent workflow."""
    try:
        # Mock implementation - replace with actual agent orchestrator
        keywords = request_data.get("keywords", "")
        location = request_data.get("location", "")
        experience_level = request_data.get("experience_level", "")
        job_type = request_data.get("job_type", "")
        max_results = request_data.get("max_results", 50)
        
        # TODO: Initialize and run the actual agent orchestrator
        # orchestrator = AgentOrchestrator()
        # results = await orchestrator.execute_job_search_workflow(
        #     user_id="demo_user",
        #     search_criteria=request_data
        # )
        
        # Mock response for now
        mock_jobs = [
            {
                "title": f"Senior {keywords} Developer",
                "company": "TechCorp Inc.",
                "location": location or "Remote",
                "job_type": job_type or "Full-time",
                "description": f"We are looking for an experienced {keywords} developer to join our team...",
                "match_score": 85,
                "url": "https://example.com/job1"
            },
            {
                "title": f"{keywords} Engineer",
                "company": "StartupXYZ",
                "location": location or "San Francisco, CA",
                "job_type": job_type or "Full-time",
                "description": f"Join our innovative team as a {keywords} engineer working on cutting-edge projects...",
                "match_score": 78,
                "url": "https://example.com/job2"
            }
        ]
        
        return {
            "status": "success",
            "message": f"Found {len(mock_jobs)} job opportunities",
            "jobs": mock_jobs,
            "search_criteria": request_data
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Job search failed: {str(e)}",
            "jobs": []
        }


@app.post("/api/agent/run")
async def run_auto_apply_agent(request_data: dict):
    """Run the AutoAgentHire browser automation agent."""
    try:
        from backend.agents.auto_apply_agent_clean import run_autoagent
        
        # Extract parameters
        job_criteria = request_data.get("job_criteria", {})
        keywords = job_criteria.get("keywords", "software engineer")
        location = job_criteria.get("location", "Remote")
        max_applications = request_data.get("max_applications", 5)
        resume_path = request_data.get("resume_path", "data/resumes/default_resume.txt")
        
        logger.info(f"🤖 Starting AutoAgent with criteria: {job_criteria}")
        
        # Run the AutoAgent
        result = await run_autoagent(
            keyword=keywords,
            location=location,
            resume_path=resume_path,
            max_jobs=max_applications,
            auto_apply=True
        )
        
        return {
            "status": "success",
            "message": "AutoAgent completed successfully",
            "results": result
        }
        
    except Exception as e:
        logger.error(f"❌ AutoAgent failed: {str(e)}")
        return {
            "status": "error",
            "message": f"AutoAgent failed: {str(e)}"
        }


@app.get("/api/agent/status")
async def get_agent_status():
    """Get the current status of the AutoAgent."""
    try:
        return {
            "status": "ready",
            "message": "AutoAgent is ready to run",
            "last_run": None,
            "applications_submitted": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Status check failed: {str(e)}"
        }


@app.post("/api/run-agent")
async def trigger_autoagent(request_data: dict):
    """Trigger the AutoAgent with job search and auto-apply."""
    try:
        from backend.agents.auto_apply_agent_clean import run_autoagent
        
        # Extract user preferences
        preferences = request_data.get("preferences", {})
        keywords = preferences.get("job_title", "AI Engineer")
        location = preferences.get("location", "Remote")
        experience_level = preferences.get("experience_level", "mid")
        resume_path = preferences.get("resume_path", "data/resumes/default_resume.txt")
        
        logger.info(f"🚀 Triggering AutoAgent with preferences: {preferences}")
        
        # Start the automated job search and application process
        result = await run_autoagent(
            keyword=keywords,
            location=location,
            resume_path=resume_path,
            experience_level=experience_level,
            max_jobs=5,
            auto_apply=True
        )
        
        return {
            "status": "success",
            "message": "AutoAgent started successfully",
            "data": result,
            "execution_summary": result.get("execution_summary", {})
        }
        
    except Exception as e:
        logger.error(f"❌ AutoAgent trigger failed: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to start AutoAgent: {str(e)}"
        }


# File upload and agent endpoints  
from fastapi import UploadFile, File, Form
import aiofiles
import tempfile


@app.post("/api/run-agent-with-file")
async def run_agent_with_resume(
    file: UploadFile = File(...),
    keyword: str = Form("AI Engineer"),
    location: str = Form("Remote"),
    max_jobs: int = Form(10),
    similarity_threshold: float = Form(0.5)
):
    """
    Run AutoAgent LinkedIn automation with resume upload.
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return {
                "status": "error",
                "message": "Only PDF files are supported for resume upload"
            }
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Import and run the AutoAgent service
            from backend.agents.auto_apply_agent_clean import run_autoagent
            
            logger.info(f"🚀 Starting AutoAgent for keyword: '{keyword}' in location: '{location}'")
            
            # Run the automation
            results = await run_autoagent(
                keyword=keyword,
                location=location,
                resume_path=temp_file_path,
                max_jobs=max_jobs,
                similarity_threshold=similarity_threshold,
                auto_apply=True
            )
            
            # Check for errors in results
            if "error" in results:
                return {
                    "status": "error",
                    "message": results["error"]
                }
            
            return {
                "status": "success",
                "message": "AutoAgent automation completed successfully",
                "data": results
            }
            
        finally:
            # Clean up temporary file
            import os
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        logger.error(f"❌ Run Agent error: {str(e)}")
        return {
            "status": "error",
            "message": f"Automation failed: {str(e)}"
        }


# Include routers
from backend.routes.agent import router as agent_router
app.include_router(agent_router, tags=["AutoAgent"])


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
