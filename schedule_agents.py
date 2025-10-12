#!/usr/bin/env python3
"""
AutoAgentHire - Scheduled Agent Runner
Runs agents on a schedule for continuous job monitoring.
"""
import asyncio
import schedule
import time
from datetime import datetime
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.agents.orchestrator import AgentOrchestrator
from backend.config import settings


class ScheduledJobRunner:
    """Runs job search agents on a schedule."""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.default_search_criteria = {
            "keywords": "Python Developer",
            "location": "Remote",
            "experience_level": "Mid Level",
            "job_type": "Full-time",
            "max_results": 20,
            "auto_apply": False
        }
    
    async def run_scheduled_search(self, search_criteria=None):
        """Run a scheduled job search."""
        criteria = search_criteria or self.default_search_criteria
        
        print(f"🕒 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled job search...")
        print(f"🔍 Searching for: {criteria['keywords']}")
        
        try:
            results = await self.orchestrator.execute_job_search_workflow(
                user_id="scheduled_user",
                search_criteria=criteria
            )
            
            print(f"✅ Found {results.get('jobs_found', 0)} jobs")
            if results.get('applications_sent', 0) > 0:
                print(f"📧 Sent {results['applications_sent']} applications")
            
            return results
            
        except Exception as e:
            print(f"❌ Scheduled search failed: {str(e)}")
            return None
    
    def schedule_jobs(self):
        """Set up job schedules."""
        print("⏰ Setting up scheduled job searches...")
        
        # Schedule different searches
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.run_scheduled_search())
        ).tag('daily_search')
        
        schedule.every().monday.at("08:00").do(
            lambda: asyncio.run(self.run_scheduled_search({
                **self.default_search_criteria,
                "keywords": "Senior Python Developer",
                "max_results": 50
            }))
        ).tag('weekly_senior_search')
        
        schedule.every().friday.at("17:00").do(
            lambda: asyncio.run(self.run_scheduled_search({
                **self.default_search_criteria,
                "keywords": "Machine Learning Engineer",
                "location": "San Francisco"
            }))
        ).tag('weekly_ml_search')
        
        print("📅 Scheduled jobs:")
        print("  - Daily search at 9:00 AM")
        print("  - Weekly senior roles on Monday 8:00 AM")
        print("  - Weekly ML roles on Friday 5:00 PM")
    
    def run_scheduler(self):
        """Run the job scheduler."""
        print("🚀 Starting AutoAgentHire Scheduler...")
        self.schedule_jobs()
        
        print("⏳ Waiting for scheduled jobs... (Press Ctrl+C to stop)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n🛑 Scheduler stopped by user")
        except Exception as e:
            print(f"❌ Scheduler error: {str(e)}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
AutoAgentHire Scheduler - Automated Job Search Agent

Usage:
  python schedule_agents.py          # Start the scheduler
  python schedule_agents.py --help   # Show this help

Features:
  🕒 Automated daily job searches
  📊 Weekly specialized searches
  📧 Optional auto-application
  📝 Detailed logging

Schedule:
  - 09:00 Daily: General Python Developer search
  - 08:00 Monday: Senior Python Developer search  
  - 17:00 Friday: Machine Learning Engineer search

Configuration:
  Edit the default_search_criteria in the script to customize searches.
        """)
        return
    
    runner = ScheduledJobRunner()
    runner.run_scheduler()


if __name__ == "__main__":
    main()