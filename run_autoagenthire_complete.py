"""
AutoAgentHire - Complete Runner (Direct Automation)
This script runs the automation directly with improved network handling
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
    """Run AutoAgentHire with improved configuration"""
    
    print("=" * 70)
    print("🤖 AutoAgentHire - LinkedIn Job Automation")
    print("=" * 70)
    print()
    
    # Configuration
    config = {
        'resume_path': './data/resumes/resume.txt',
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, Machine Learning, AI, Deep Learning, TensorFlow',
        'max_jobs': 5,
        'similarity_threshold': 0.6,
        'auto_apply': True,
        'experience_level': 'Entry level',  # Entry level, Associate, Mid-Senior level, Director, Executive
        'job_type': 'Full-time'  # Full-time, Part-time, Contract, Temporary, Internship
    }
    
    print("📋 Configuration:")
    print(f"  Resume: {config['resume_path']}")
    print(f"  Keyword: {config['keyword']}")
    print(f"  Location: {config['location']}")
    print(f"  Skills: {config['skills']}")
    print(f"  Max Jobs: {config['max_jobs']}")
    print(f"  Auto-Apply: {config['auto_apply']}")
    print(f"  Experience: {config['experience_level']}")
    print(f"  Job Type: {config['job_type']}")
    print()
    
    # Check credentials
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not linkedin_email or not linkedin_password:
        print("❌ Error: LinkedIn credentials not found in .env file")
        print("   Please add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to .env")
        return
    
    if not gemini_api_key:
        print("⚠️  Warning: GEMINI_API_KEY not found. AI analysis will be limited.")
    
    print("🚀 Starting automation...")
    print("=" * 70)
    print()
    
    # Create bot and run
    bot = AutoAgentHireBot(config)
    
    try:
        result = await bot.run_automation()
        
        print()
        print("=" * 70)
        print("✅ AUTOMATION COMPLETE!")
        print("=" * 70)
        print()
        print("📊 Summary:")
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
        
        print("=" * 70)
        print("📁 Full report saved in reports/ directory")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Automation failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run automation
    asyncio.run(main())
