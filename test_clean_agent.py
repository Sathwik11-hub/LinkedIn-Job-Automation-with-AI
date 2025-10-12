#!/usr/bin/env python3
"""
Test the clean Auto Apply Agent
"""
import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_clean_agent():
    """Test the clean auto apply agent."""
    print("🚀 Testing Clean Auto Apply Agent")
    print("=" * 50)
    
    try:
        from backend.agents.auto_apply_agent_clean import AutoApplyAgent, run_autoagent
        print("✅ Successfully imported clean agent")
        
        # Test agent initialization
        agent = AutoApplyAgent()
        print("✅ Agent initialized")
        
        # Test browser
        success = await agent.initialize_browser(headless=True)
        if success:
            print("✅ Browser initialized")
            
            # Test login
            login_success = await agent.login_to_linkedin()
            if login_success:
                print("✅ LinkedIn login successful")
                
                # Test job search
                jobs = await agent.search_jobs("Python Developer", "Remote")
                print(f"✅ Found {len(jobs)} jobs")
                
                if jobs:
                    # Test AI analysis
                    analysis = await agent.analyze_job_compatibility(jobs[0], "Python developer with 5 years experience")
                    print(f"✅ AI analysis: Score {analysis['score']}/10")
            else:
                print("❌ LinkedIn login failed")
        else:
            print("❌ Browser initialization failed")
        
        await agent.close_browser()
        print("✅ All tests completed")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(test_clean_agent())