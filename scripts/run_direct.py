#!/usr/bin/env python3
"""
Direct AutoAgentHire Runner - Runs without problematic dependencies
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def main():
    """Run the AutoAgentHire automation directly"""
    
    print("\n" + "="*60)
    print("🤖 AutoAgentHire - Direct Runner")
    print("="*60)
    
    # Import bot
    try:
        from backend.agents.autoagenthire_bot import AutoAgentHireBot
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nTrying to install missing dependencies...")
        os.system("pip install playwright google-generativeai PyPDF2 python-dotenv")
        from backend.agents.autoagenthire_bot import AutoAgentHireBot
    
    # Get resume path
    resume_path = input("\n📄 Enter path to your resume PDF (or press Enter for sample): ").strip()
    if not resume_path:
        resume_path = "./data/resumes/resume.txt"  # Use sample
    
    # Configuration
    config = {
        'resume_path': resume_path,
        'keyword': input("🔍 Job keyword (default: AI Engineer): ").strip() or "AI Engineer",
        'location': input("📍 Location (default: Remote): ").strip() or "Remote",
        'skills': input("💡 Skills (default: Python, ML, AI): ").strip() or "Python, Machine Learning, AI",
        'experience_level': 'Any',
        'job_type': 'Any',
        'salary_range': 'Any',
        'max_jobs': int(input("📊 Max jobs to apply (default: 5): ").strip() or 5),
        'similarity_threshold': 0.6,
        'auto_apply': input("✅ Auto-apply? (yes/no, default: yes): ").strip().lower() != 'no'
    }
    
    print(f"\n📋 Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    confirm = input("\n🚀 Start automation? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("❌ Cancelled")
        return
    
    # Run bot
    bot = AutoAgentHireBot(config)
    
    try:
        result = await bot.run_automation()
        
        print("\n" + "="*60)
        print("✅ AUTOMATION COMPLETE!")
        print("="*60)
        print(f"📊 Jobs Found: {result['jobs_found']}")
        print(f"🤖 Jobs Analyzed: {result['jobs_analyzed']}")
        print(f"📝 Applications Attempted: {result['applications_attempted']}")
        print(f"✅ Applications Successful: {result['applications_successful']}")
        print(f"📈 Success Rate: {result['applications_successful']}/{result['applications_attempted']}")
        
        if result.get('errors'):
            print(f"\n⚠️  Errors: {len(result['errors'])}")
            for error in result['errors'][:5]:
                print(f"  - {error}")
        
        # Show top jobs
        if result.get('jobs'):
            print(f"\n🎯 Top Jobs:")
            for i, job in enumerate(result['jobs'][:5], 1):
                print(f"\n{i}. {job['title']} at {job['company']}")
                print(f"   📍 {job['location']}")
                print(f"   🎯 Match: {job.get('similarity_score', 0)}%")
                print(f"   📋 Status: {job.get('application_status', 'N/A')}")
        
        print("\n" + "="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
