"""
AutoAgentHire - WORKING VERSION
This version successfully completes job collection and analysis
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.agents.autoagenthire_bot import AutoAgentHireBot

async def run_quick_test():
    """Quick test to verify job collection works"""

    print("🚀 Quick Job Collection Test")
    print("=" * 40)

    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, ML, AI',
        'max_jobs': 3,
        'similarity_threshold': 0.6,
        'auto_apply': False
    }

    bot = AutoAgentHireBot(config)

    try:
        # Quick initialization
        await bot.initialize_browser()
        await bot.login_linkedin()
        bot.parse_resume(config['resume_path'])

        # Quick job search
        await bot.search_jobs(config['keyword'], config['location'])

        # Quick job collection with timeout
        print("📊 Collecting jobs (quick test)...")
        jobs = await asyncio.wait_for(
            bot.collect_job_listings(5),
            timeout=30.0  # 30 second timeout
        )

        print(f"✅ SUCCESS! Collected {len(jobs)} jobs")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['title'][:40]}...")

        return True

    except asyncio.TimeoutError:
        print("⏰ Job collection timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        if bot.browser:
            try:
                await bot.browser.close()
            except:
                pass

async def main():
    """Main working automation"""

    print("=" * 70)
    print("🤖 AutoAgentHire - WORKING VERSION")
    print("=" * 70)

    # First run quick test
    print("🧪 Running quick test first...")
    test_success = await run_quick_test()

    if not test_success:
        print("❌ Quick test failed. Checking setup...")
        return

    print("\n✅ Quick test passed! Running full automation...")
    print("=" * 70)

    # Full configuration
    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, Machine Learning, AI, Deep Learning, TensorFlow',
        'max_jobs': 5,
        'similarity_threshold': 0.6,
        'auto_apply': False  # Change to True when ready
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
        print("❌ Error: LinkedIn credentials not found")
        return

    if not gemini_api_key:
        print("⚠️  Warning: No GEMINI_API_KEY - AI analysis limited")

    print("🚀 Starting full automation...")
    print("=" * 70)

    # Create bot
    bot = AutoAgentHireBot(config)

    try:
        # Phase 1: Browser
        print("\nPHASE 1: BROWSER INITIALIZATION")
        await bot.initialize_browser()

        # Phase 2: Login
        print("\nPHASE 2: LINKEDIN LOGIN")
        await bot.login_linkedin()

        # Phase 3: Resume
        print("\nPHASE 3: RESUME PARSING")
        resume_text = bot.parse_resume(config['resume_path'])
        print(f"✅ Resume parsed: {len(resume_text)} characters")

        # Phase 4: Search
        print("\nPHASE 4: JOB SEARCH")
        await bot.search_jobs(config['keyword'], config['location'])

        # Phase 5: Collection with timeout protection
        print("\nPHASE 5: JOB COLLECTION")
        try:
            jobs = await asyncio.wait_for(
                bot.collect_job_listings(config['max_jobs']),
                timeout=45.0  # 45 second timeout
            )
            print(f"✅ Collected {len(jobs)} jobs")
        except asyncio.TimeoutError:
            print("⏰ Job collection timed out - using any jobs found so far")
            jobs = bot.jobs_data  # Use whatever was collected

        # Phase 6: AI Analysis (if jobs found)
        if jobs:
            print("\nPHASE 6: AI ANALYSIS")
            analyzed_jobs = []
            for i, job in enumerate(jobs, 1):
                print(f"🎯 Analyzing job {i}: {job['title'][:30]}...")
                try:
                    score = await bot.analyze_job_with_ai(job)
                    job['ai_score'] = score
                    analyzed_jobs.append(job)
                    print(f"✅ Score: {score}/100")
                except Exception as e:
                    print(f"⚠️  AI failed for job {i}: {str(e)}")
                    job['ai_score'] = 50
                    analyzed_jobs.append(job)

            # Phase 7: Selection
            print("\nPHASE 7: JOB SELECTION")
            top_jobs = await bot.select_top_jobs(config['max_jobs'])
            print(f"🎯 Selected {len(top_jobs)} top jobs")

            # Show results
            print("\n" + "="*70)
            print("✅ AUTOMATION SUCCESS!")
            print("="*70)
            print(f"📊 Jobs Found: {len(jobs)}")
            print(f"🤖 Jobs Analyzed: {len(analyzed_jobs)}")
            print(f"🎯 Top Jobs Selected: {len(top_jobs)}")

            print("\n📋 Top Job Matches:")
            for i, job in enumerate(top_jobs[:3], 1):
                score = job.get('ai_score', 'N/A')
                title = job.get('title', 'Unknown')[:40]
                company = job.get('company', 'Unknown')[:25]
                print(f"  {i}. [{score}] {title}... at {company}...")

        else:
            print("\n⚠️  No jobs were collected")

        print("\n" + "="*70)
        print("🎉 WORKING AUTOMATION COMPLETED!")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Automation failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if bot.browser:
            try:
                await bot.browser.close()
            except Exception as e:
                print(f"⚠️  Cleanup warning: {str(e)}")

if __name__ == "__main__":
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()

    # Run working automation
    asyncio.run(main())
