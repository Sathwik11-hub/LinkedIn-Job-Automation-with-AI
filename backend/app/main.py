from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, jobs, applications, reports
from app.core.config import settings
from app.core.database import engine, Base
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoAgentHire API",
    description="AI-Powered LinkedIn Job Application Automation System",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/v1/applications", tags=["applications"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])

@app.get("/")
async def root():
    return {
        "message": "AutoAgentHire API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )