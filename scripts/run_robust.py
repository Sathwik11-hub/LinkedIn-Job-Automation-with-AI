"""
AutoAgentHire - Robust Version
Handles interruptions gracefully and focuses on job collection
"""

import asyncio
import os
import sys
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.agents.autoagenthire_bot import AutoAgentHireBot

class GracefulInterrupt:
    """Handle Ctrl+C gracefully"""
    def __init__(self):
        self.interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("\n⚠️  Received interrupt signal. Finishing current operation...")
        self.interrupted = True

async def main():
    """Run robust automation with graceful interruption handling"""

    interrupt_handler = GracefulInterrupt()

    print("=" * 70)
    print("🤖 AutoAgentHire - Robust Version")
    print("=" * 70)

    # Configuration
    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, Machine Learning, AI, Deep Learning, TensorFlow',
        'max_jobs': 5,
        'similarity_threshold': 0.6,
        'auto_apply': False  # Test without applying first
    }

    print("📋 Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()

    # Check credentials
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not linkedin_email or not linkedin_password:
        print("❌ Error: LinkedIn credentials not found in .env file")
        return

    if not gemini_api_key:
        print("⚠️  Warning: GEMINI_API_KEY not found. AI analysis will be limited.")

    print("🚀 Starting robust automation...")
    print("=" * 70)

    # Create bot
    bot = AutoAgentHireBot(config)

    try:
        # Phase 1: Browser initialization
        print("\n" + "="*60)
        print("PHASE 1: BROWSER INITIALIZATION")
        print("="*60)
        await bot.initialize_browser()

        if interrupt_handler.interrupted:
            print("⚠️  Interrupted during browser initialization")
            return

        # Phase 2: LinkedIn login
        print("\n" + "="*60)
        print("PHASE 2: LINKEDIN LOGIN")
        print("="*60)
        await bot.login_linkedin()

        if interrupt_handler.interrupted:
            print("⚠️  Interrupted during login")
            return

        # Phase 3: Resume parsing
        print("\n" + "="*60)
        print("PHASE 3: RESUME PARSING")
        print("="*60)
        resume_text = bot.parse_resume(config['resume_path'])
        print(f"✅ Resume parsed: {len(resume_text)} characters")

        if interrupt_handler.interrupted:
            print("⚠️  Interrupted during resume parsing")
            return

        # Phase 4: Job search
        print("\n" + "="*60)
        print("PHASE 4: JOB SEARCH")
        print("="*60)
        await bot.search_jobs(config['keyword'], config['location'])

        if interrupt_handler.interrupted:
            print("⚠️  Interrupted during job search")
            return

        # Phase 5: Job collection
        print("\n" + "="*60)
        print("PHASE 5: COLLECTING JOB LISTINGS")
        print("="*60)
        jobs = await bot.collect_job_listings(config['max_jobs'])

        print(f"\n✅ SUCCESS! Collected {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['title'][:50]}... at {job['company'][:30]}...")

        if interrupt_handler.interrupted:
            print("⚠️  Interrupted during job collection")
            return

        # Phase 6: AI Analysis (if we have jobs and API key)
        if jobs and gemini_api_key and not interrupt_handler.interrupted:
            print("\n" + "="*60)
            print("PHASE 6: AI JOB ANALYSIS")
            print("="*60)

            analyzed_jobs = []
            for i, job in enumerate(jobs, 1):
                if interrupt_handler.interrupted:
                    break

                print(f"🎯 Analyzing job {i}/{len(jobs)}: {job['title'][:30]}...")
                try:
                    score = await bot.analyze_job_with_ai(job)
                    job['ai_score'] = score
                    analyzed_jobs.append(job)
                    print(f"✅ Score: {score}/100")
                except Exception as e:
                    print(f"⚠️  AI analysis failed for job {i}: {str(e)}")
                    job['ai_score'] = 50  # Default score
                    analyzed_jobs.append(job)

            # Select top jobs
            top_jobs = await bot.select_top_jobs(config['max_jobs'])
            print(f"\n🎯 Selected {len(top_jobs)} top jobs for application")

        print("\n" + "="*70)
        print("✅ ROBUST AUTOMATION COMPLETED!")
        print("="*70)

        if jobs:
            print(f"📊 Results: {len(jobs)} jobs collected")
            if 'top_jobs' in locals():
                print(f"🎯 Top jobs selected: {len(top_jobs)}")
        else:
            print("📊 Results: No jobs collected")

    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Automation failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if bot.browser:
            print("\n🧹 Cleaning up...")
            try:
                await bot.browser.close()
            except Exception as e:
                print(f"⚠️  Browser cleanup warning: {str(e)}")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run robust automation
    asyncio.run(main())
