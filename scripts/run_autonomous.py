"""
AutoAgentHire - Autonomous Version
Runs completely without user interaction
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
    """Run fully autonomous automation"""

    print("=" * 80)
    print("🤖 AutoAgentHire - FULLY AUTONOMOUS MODE")
    print("=" * 80)

    # Configuration for autonomous operation
    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, Machine Learning, AI, Deep Learning, TensorFlow',
        'max_jobs': 5,
        'similarity_threshold': 0.6,
        'auto_apply': False  # Set to True when ready to apply
    }

    print("📋 Autonomous Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()

    # Validate environment
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    if not linkedin_email or not linkedin_password:
        print("❌ Error: LinkedIn credentials not found in .env file")
        print("   Please add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to .env")
        return

    if not gemini_api_key:
        print("⚠️  Warning: GEMINI_API_KEY not found. AI analysis will be limited.")
        print("   Add GEMINI_API_KEY to .env for full functionality")

    print("🚀 Starting fully autonomous automation...")
    print("=" * 80)
    print()

    # Create bot and run complete automation
    bot = AutoAgentHireBot(config)

    try:
        result = await bot.run_automation()

        print()
        print("=" * 80)
        print("✅ AUTONOMOUS AUTOMATION COMPLETED!")
        print("=" * 80)
        print()
        print("📊 Final Results:")
        print(f"  Jobs Found: {result.get('jobs_found', 0)}")
        print(f"  Jobs Analyzed: {result.get('jobs_analyzed', 0)}")
        print(f"  Applications Attempted: {result.get('applications_attempted', 0)}")
        print(f"  Applications Successful: {result.get('applications_successful', 0)}")
        print()

        if result.get('errors'):
            print(f"⚠️  Errors ({len(result['errors'])}):")
            for error in result['errors']:
                print(f"  - {error}")
            print()

        print("=" * 80)
        print("📁 Full report saved in reports/ directory")
        print("🎯 Check the latest JSON report for detailed results")
        print("=" * 80)

        # Show summary of jobs if available
        if result.get('jobs'):
            print(f"\n📋 Job Summary ({len(result['jobs'])} jobs):")
            for i, job in enumerate(result['jobs'][:5], 1):  # Show first 5
                score = job.get('ai_score', 'N/A')
                title = job.get('title', 'Unknown')[:40]
                company = job.get('company', 'Unknown')[:25]
                print(f"  {i}. [{score}] {title}... at {company}...")

    except Exception as e:
        print(f"\n\n❌ Autonomous automation failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Run autonomous automation
    asyncio.run(main())
