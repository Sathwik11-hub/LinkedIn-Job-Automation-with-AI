"""
AutoAgentHire FastAPI Endpoints
Handles frontend requests and automation orchestration
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import asyncio
from typing import Optional

from backend.agents.autoagenthire_bot import AutoAgentHireBot

router = APIRouter(prefix="/api", tags=["AutoAgentHire"])

# Store active automation tasks
active_tasks = {}


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@router.get("/agent/status")
async def agent_status():
    """Check if agents are configured"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    gemini_configured = bool(gemini_key and not gemini_key.startswith('your_'))
    linkedin_configured = bool(os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD'))
    
    return {
        "agents": {
            "gemini_ai": "configured" if gemini_configured else "not_configured",
            "linkedin": "configured" if linkedin_configured else "not_configured"
        }
    }


@router.post("/run-agent")
async def run_agent(
    file: UploadFile = File(...),
    keyword: str = Form(...),
    location: str = Form(...),
    skills: str = Form(...),
    experience_level: str = Form("Any"),
    job_type: str = Form("Any"),
    salary_range: str = Form("Any"),
    max_jobs: int = Form(15),
    similarity_threshold: float = Form(0.6),
    auto_apply: bool = Form(True)
):
    """
    Run the complete AutoAgentHire automation
    
    Process:
    1. Save uploaded resume
    2. Initialize automation bot
    3. Run complete workflow
    4. Return results
    """
    
    try:
        # Validate resume file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
            
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF resumes are accepted")
        
        # Save resume to temp location
        resume_dir = Path("uploads/resumes")
        resume_dir.mkdir(parents=True, exist_ok=True)
        
        resume_path = resume_dir / file.filename
        
        # Save file content
        with open(resume_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        print(f"📄 Resume saved: {resume_path}")
        
        # Prepare configuration
        config = {
            'resume_path': str(resume_path),
            'keyword': keyword,
            'location': location,
            'skills': skills,
            'experience_level': experience_level,
            'job_type': job_type,
            'salary_range': salary_range,
            'max_jobs': min(max_jobs, 50),  # Safety limit
            'similarity_threshold': similarity_threshold,
            'auto_apply': auto_apply
        }
        
        print("\n🤖 Starting AutoAgentHire automation...")
        print(f"📋 Config: {config}")
        
        # Initialize and run bot
        bot = AutoAgentHireBot(config)
        result = await bot.run_automation()
        
        # Prepare response
        response = {
            "status": "success" if result['applications_successful'] > 0 or len(result['jobs']) > 0 else "partial",
            "message": result['summary'],
            "data": result
        }
        
        # Save report
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        
        import json
        from datetime import datetime
        
        report_file = report_dir / f"autoagenthire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Report saved: {report_file}")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e),
                "data": {
                    "jobs_found": 0,
                    "jobs_analyzed": 0,
                    "applications_attempted": 0,
                    "applications_successful": 0,
                    "jobs": [],
                    "summary": f"Error: {str(e)}",
                    "errors": [str(e)]
                }
            }
        )


@router.get("/reports/latest")
async def get_latest_report():
    """Get the most recent automation report"""
    try:
        report_dir = Path("reports")
        
        if not report_dir.exists():
            return {"status": "no_reports", "data": None}
        
        reports = sorted(report_dir.glob("autoagenthire_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if not reports:
            return {"status": "no_reports", "data": None}
        
        import json
        with open(reports[0], 'r') as f:
            data = json.load(f)
        
        return {"status": "success", "data": data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def register_autoagenthire_routes(app):
    """Register AutoAgentHire routes with the main app"""
    app.include_router(router)
    print("✅ AutoAgentHire routes registered")
