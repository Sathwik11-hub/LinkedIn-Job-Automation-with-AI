"""
AutoAgentHire - Simple Test Version
This version focuses on getting job collection working reliably
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.agents.autoagenthire_bot import AutoAgentHireBot

async def main():
    """Run a simplified test of the automation"""

    print("=" * 60)
    print("🤖 AutoAgentHire - Simple Test")
    print("=" * 60)

    # Simple configuration
    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, ML, AI',
        'max_jobs': 3,  # Start small
        'similarity_threshold': 0.6,
        'auto_apply': False  # Don't apply yet, just collect jobs
    }

    print("📋 Test Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()

    # Check credentials
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    if not linkedin_email or not linkedin_password:
        print("❌ Error: LinkedIn credentials not found in .env file")
        return

    print("🚀 Starting simplified test...")
    print("=" * 60)

    # Create bot
    bot = AutoAgentHireBot(config)

    try:
        # Just test job collection
        print("\n🔧 Testing browser initialization...")
        await bot.initialize_browser()

        print("\n🔐 Testing login...")
        await bot.login_linkedin()

        print("\n📄 Testing resume parsing...")
        resume_text = bot.parse_resume(config['resume_path'])
        print(f"✅ Resume parsed: {len(resume_text)} characters")

        print("\n🔍 Testing job search...")
        await bot.search_jobs(config['keyword'], config['location'])

        print("\n📊 Testing job collection...")
        jobs = await bot.collect_job_listings(config['max_jobs'])

        print(f"\n✅ SUCCESS! Collected {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"  {i}. {job['title'][:40]}... at {job['company'][:25]}...")

        print("\n🎉 Test completed successfully!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if bot.browser:
            try:
                await bot.browser.close()
            except:
                pass

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run test
    asyncio.run(main())
