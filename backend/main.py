"""
Main FastAPI application entry point.
Initializes the application, middleware, and routes.
"""
from typing import Optional, Dict, Any
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn

from backend.config import settings
from backend.routes.api_routes import router as api_router
# from backend.utils.logger import setup_logger

# Setup logger
# logger = setup_logger(__name__)


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
    allow_origins=settings.cors_origins_list if hasattr(settings, 'cors_origins_list') else settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip Middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(api_router)


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


# Simple API to run the automation agent (mocked for local dev)
@app.post("/api/run-agent")
async def run_agent(background_tasks: BackgroundTasks, payload: Optional[Dict[str, Any]] = None):
    """Trigger the agent orchestrator to search and apply for jobs.

    Accepts a JSON payload with search criteria. Example:
      {"keywords": "AI Engineer", "location": "Remote", "linkedin_email": "...", "linkedin_password": "...", "submit": false}
    """
    from backend.agents.orchestrator import AgentOrchestrator

    data = payload or {}
    orchestrator = AgentOrchestrator()

    async def _run_task(criteria: dict):
        await orchestrator.execute_job_search_workflow(user_id="local_user", search_criteria=criteria)

    background_tasks.add_task(_run_task, data)
    return {"status": "started", "message": "Agent started in background"}


@app.get("/api/agent/status")
async def agent_status():
    """Return status of last agent run."""
    from backend.agents.state import get_status

    return get_status()


# Include AutoAgentHire routes
try:
    from backend.api.autoagenthire import register_autoagenthire_routes
    register_autoagenthire_routes(app)
except Exception as e:
    print(f"⚠️  Could not load AutoAgentHire routes: {e}")

# TODO: Include routers
# app.include_router(routes.auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(routes.jobs_router, prefix="/jobs", tags=["Jobs"])
# app.include_router(routes.applications_router, prefix="/applications", tags=["Applications"])
# app.include_router(routes.user_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
