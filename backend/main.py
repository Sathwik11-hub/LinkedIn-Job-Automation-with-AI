"""
Main FastAPI application entry point.
Initializes the application, middleware, and routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import uvicorn

from backend.config import settings
# from backend.api import routes
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
    allow_origins=settings.CORS_ORIGINS,
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
