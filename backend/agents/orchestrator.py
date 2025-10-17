"""
Agent Orchestrator - Coordinates multiple agents.
Uses CrewAI Crew to manage agent workflow.
"""
from typing import Dict, Any
# from crewai import Crew, Process
# from backend.agents.job_search_agent import JobSearchAgent
# from backend.agents.analysis_agent import AnalysisAgent
# from backend.agents.application_agent import ApplicationAgent


class AgentOrchestrator:
    """
    Orchestrates multiple agents in a coordinated workflow.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all agents."""
        # TODO: Initialize all agents
        # self.job_search_agent = JobSearchAgent()
        # self.analysis_agent = AnalysisAgent()
        # self.application_agent = ApplicationAgent()
        pass
    
    async def execute_job_search_workflow(
        self,
        user_id: str,
        search_criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the complete job search and application workflow.
        
        Workflow:
        1. Job Search Agent discovers opportunities
        2. Analysis Agent evaluates and ranks jobs
        3. Application Agent handles top matches
        
        Args:
            user_id: User identifier
            search_criteria: Job search parameters
            
        Returns:
            Workflow execution results
        """
        # Realistic (but minimal) implementation using LinkedInBot
        from backend.agents.linkedin_bot import LinkedInBot
        from backend.agents.state import set_status
        from backend.config import settings
        import os

        set_status("running", {"phase": "starting"})

        # Use credentials from search_criteria, fall back to .env file
        linkedin_email = search_criteria.get("linkedin_email") or settings.LINKEDIN_EMAIL or os.getenv("LINKEDIN_EMAIL", "")
        linkedin_password = search_criteria.get("linkedin_password") or settings.LINKEDIN_PASSWORD or os.getenv("LINKEDIN_PASSWORD", "")
        
        # Get headless setting from environment (default False to show browser)
        headless_mode = os.getenv("HEADLESS_MODE", "false").lower() in ["true", "1", "yes"]
        
        if not linkedin_email or not linkedin_password:
            set_status("failed", {"reason": "missing_credentials", "message": "LinkedIn credentials not provided"})
            return {"status": "failed", "reason": "missing_credentials", "message": "Please provide LinkedIn credentials"}

        bot = LinkedInBot(
            email=linkedin_email,
            password=linkedin_password,
            headless=headless_mode,  # Show browser by default
        )

        try:
            set_status("running", {"phase": "login", "message": f"Logging in as {linkedin_email}"})
            ok = await bot.login()
            if not ok:
                set_status("failed", {"reason": "login_failed", "message": "Could not log into LinkedIn. Check credentials or CAPTCHA."})
                return {"status": "failed", "reason": "login_failed", "message": "Login failed - check credentials"}

            keywords = search_criteria.get("keywords", "") or os.getenv("JOB_KEYWORDS", "Python Developer")
            location = search_criteria.get("location", "") or os.getenv("JOB_LOCATION", "Remote")
            
            set_status("running", {"phase": "searching", "message": f"Searching for: {keywords} in {location}"})
            jobs = await bot.search_jobs(keywords, location)
            
            set_status("running", {"phase": "found_jobs", "jobs_count": len(jobs), "message": f"Found {len(jobs)} jobs"})

            submit = bool(search_criteria.get("submit", False))
            set_status("running", {"phase": "applying", "jobs": len(jobs), "submit": submit})
            results = []
            for job in jobs:
                url = job.get("url") or job.get("link")
                if not url:
                    continue
                if not submit:
                    preview = await bot.prepare_application(url)
                    results.append({"url": url, "preview": preview})
                else:
                    res = await bot.submit_application(url)
                    results.append(res)

            # Persist previews or results
            try:
                from backend.agents.storage import save_application_result
                for r in results:
                    save_application_result({"user_id": user_id, "result": r})
            except Exception:
                pass

            set_status("completed", {"jobs_found": len(jobs), "results": results})
            applied_count = len([r for r in results if r.get("status") == "applied"]) if submit else 0
            return {"jobs_found": len(jobs), "applications_created": applied_count, "status": "completed"}
        finally:
            try:
                await bot.stop()
            except Exception:
                pass
    
    async def execute_daily_automation(self) -> Dict[str, Any]:
        """
        Execute daily automation tasks for all users.
        
        Returns:
            Daily automation results
        """
        # TODO: Implement daily automation
        # 1. Get all users with automation enabled
        # 2. Run job search for each user
        # 3. Analyze new opportunities
        # 4. Send notifications
        
        return {
            "users_processed": 0,
            "jobs_found": 0,
            "notifications_sent": 0
        }
