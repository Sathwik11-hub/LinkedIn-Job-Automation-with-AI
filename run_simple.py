#!/usr/bin/env python3
"""
AutoAgentHire - Simple Runner
Runs the LinkedIn automation with preset values
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def main():
    print("\n" + "="*70)
    print("🤖 AutoAgentHire - LinkedIn Job Automation")
    print("="*70)
    
    # Import bot (with better error handling)
    try:
        from backend.agents.autoagenthire_bot import AutoAgentHireBot
    except ImportError as e:
        print(f"\n❌ Missing dependency: {e}")
        print("\n💡 Solution: Run this from the virtual environment:")
        print("   source venv/bin/activate && python3 run_simple.py")
        return
    
    # Simple preset configuration
    config = {
        'resume_path': './data/resumes/resume.txt',  # Sample resume
        'keyword': 'AI Engineer',
        'location': 'Remote',
        'skills': 'Python, Machine Learning, AI, Deep Learning, TensorFlow',
        'experience_level': 'Any',
        'job_type': 'Any',
        'salary_range': 'Any',
        'max_jobs': 5,
        'similarity_threshold': 0.6,
        'auto_apply': True  # Set to False for dry run
    }
    
    print("\n📋 Configuration:")
    print(f"  Resume: {config['resume_path']}")
    print(f"  Keyword: {config['keyword']}")
    print(f"  Location: {config['location']}")
    print(f"  Skills: {config['skills']}")
    print(f"  Max Jobs: {config['max_jobs']}")
    print(f"  Auto-Apply: {config['auto_apply']}")
    
    print("\n🚀 Starting automation...")
    print("="*70)
    
    # Run bot
    bot = AutoAgentHireBot(config)
    
    try:
        result = await bot.run_automation()
        
        # Display results
        print("\n" + "="*70)
        print("✅ AUTOMATION COMPLETE!")
        print("="*70)
        
        print(f"\n📊 Summary:")
        print(f"  Jobs Found: {result['jobs_found']}")
        print(f"  Jobs Analyzed: {result['jobs_analyzed']}")
        print(f"  Applications Attempted: {result['applications_attempted']}")
        print(f"  Applications Successful: {result['applications_successful']}")
        
        if result['applications_attempted'] > 0:
            success_rate = (result['applications_successful'] / result['applications_attempted']) * 100
            print(f"  Success Rate: {success_rate:.1f}%")
        
        # Show jobs
        if result.get('jobs'):
            print(f"\n🎯 Jobs Applied:")
            for i, job in enumerate(result['jobs'], 1):
                status_icon = "✅" if job.get('application_status') == 'SUCCESS' else "⏭️"
                print(f"\n{i}. {status_icon} {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Match Score: {job.get('similarity_score', 'N/A')}%")
                print(f"   Status: {job.get('application_status', 'N/A')}")
                if job.get('application_reason'):
                    print(f"   Note: {job['application_reason']}")
        
        # Show errors
        if result.get('errors'):
            print(f"\n⚠️  Errors ({len(result['errors'])}):")
            for error in result['errors'][:3]:
                print(f"  - {error}")
            if len(result['errors']) > 3:
                print(f"  ... and {len(result['errors']) - 3} more")
        
        print("\n" + "="*70)
        print("📁 Full report saved in reports/ directory")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Automation stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Stopped!")
