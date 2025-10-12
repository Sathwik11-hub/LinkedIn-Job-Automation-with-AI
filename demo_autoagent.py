#!/usr/bin/env python3
"""
AutoAgentHire Demo Script
Test the browser automation and Gemini AI integration.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def demo_autoagent():
    """Demo the AutoAgentHire functionality."""
    try:
        # Import after path setup
        from backend.agents.auto_apply_agent import run_autoagent
        
        print("🤖 AutoAgentHire Demo Starting...")
        print("=" * 50)
        
        # Demo configuration
        demo_config = {
            "keyword": "Python Developer",
            "location": "Remote", 
            "resume_text": """
            John Doe - Senior Python Developer
            
            EXPERIENCE:
            - 5+ years of Python development experience
            - Expert in Django, FastAPI, and Flask frameworks
            - Strong background in machine learning and data science
            - Experience with AWS, Docker, and Kubernetes
            - Proficient in JavaScript, React, and SQL
            
            SKILLS:
            Python, Django, FastAPI, React, AWS, Docker, Machine Learning, APIs
            
            EDUCATION:
            Bachelor's Degree in Computer Science
            """,
            "max_applications": 2,  # Limit for demo
            "headless": True  # Run in background
        }
        
        print(f"🔍 Search Keywords: {demo_config['keyword']}")
        print(f"📍 Location: {demo_config['location']}")
        print(f"📄 Resume: Loaded (sample)")
        print(f"🎯 Max Applications: {demo_config['max_applications']}")
        print("-" * 50)
        
        # Check environment variables
        gemini_key = os.getenv("GEMINI_API_KEY")
        linkedin_email = os.getenv("LINKEDIN_EMAIL")
        
        if not gemini_key or gemini_key == "your-google-gemini-api-key":
            print("⚠️  Gemini API key not configured - using mock responses")
        else:
            print("✅ Gemini API key configured")
            
        if not linkedin_email or linkedin_email == "your-email@example.com":
            print("⚠️  LinkedIn credentials not configured - demo mode only")
        else:
            print("✅ LinkedIn credentials configured")
        
        print("\n🚀 Starting automation workflow...")
        
        # Run the automation
        result = await run_autoagent(**demo_config)
        
        print("\n📊 Results:")
        print("=" * 50)
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Jobs Found: {result.get('jobs_found', 0)}")
        print(f"Applications Sent: {result.get('applications_sent', 0)}")
        
        if result.get('applications_log'):
            print("\n📋 Application History:")
            for i, app in enumerate(result['applications_log'], 1):
                print(f"{i}. {app['job_title']} at {app['company']}")
                print(f"   Status: {app['status']} | Score: {app['match_score']}%")
                print(f"   Reasoning: {app['reasoning']}")
                print()
        
        print("🎉 Demo completed!")
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install playwright google-generativeai")
        print("   playwright install chromium")
        return None
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        return None


def main():
    """Main entry point."""
    print("🤖 AutoAgentHire - Playwright + Gemini AI Demo")
    print("=" * 60)
    
    # Run the demo
    result = asyncio.run(demo_autoagent())
    
    if result:
        print("\n✅ Demo completed successfully!")
        print("\n📝 Next Steps:")
        print("1. Configure your Gemini API key in .env")
        print("2. Add LinkedIn credentials (email/password)")
        print("3. Test via API: curl -X POST http://localhost:8000/api/agent/run")
        print("4. Use the Streamlit UI for interactive automation")
    else:
        print("\n❌ Demo failed - check configuration and dependencies")


if __name__ == "__main__":
    main()