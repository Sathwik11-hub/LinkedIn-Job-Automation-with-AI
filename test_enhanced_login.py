#!/usr/bin/env python3
"""
Test script for enhanced LinkedIn login automation
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.agents.auto_apply_agent import AutoApplyAgent

async def test_enhanced_login():
    """Test the enhanced LinkedIn login functionality."""
    print("🚀 Testing enhanced LinkedIn login automation...")
    
    # Check environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    
    if not linkedin_email or not linkedin_password:
        print("❌ LinkedIn credentials not found in environment variables")
        return
    
    print(f"📧 Using LinkedIn email: {linkedin_email}")
    
    # Initialize agent (reads credentials from environment)
    agent = AutoApplyAgent()
    
    try:
        # Initialize browser (non-headless for debugging)
        print("🤖 Initializing browser with enhanced anti-detection...")
        await agent.initialize_browser(headless=False)
        print("✅ Browser initialized successfully")
        
        # Test login
        print("🔐 Testing LinkedIn login...")
        success = await agent.login_to_linkedin()
        
        if success:
            print("✅ LinkedIn login successful!")
            print("🎉 Enhanced automation is working!")
        else:
            print("❌ LinkedIn login failed")
            print("🔧 May need additional anti-detection measures")
        
        # Keep browser open for manual inspection
        print("🔍 Browser will stay open for 30 seconds for inspection...")
        await asyncio.sleep(30)
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        if hasattr(agent, 'browser') and agent.browser:
            await agent.browser.close()
            print("🧹 Browser closed")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(test_enhanced_login())