#!/usr/bin/env python3
"""
Test script for the new Run Agent functionality.
Tests the AutoAgent LinkedIn service with a sample resume.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def test_run_agent():
    """Test the Run Agent functionality."""
    print("🚀 Testing Run Agent Functionality")
    print("=" * 50)
    
    # Check environment variables
    linkedin_email = os.getenv('LINKEDIN_EMAIL')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    print(f"📧 LinkedIn Email: {'✅' if linkedin_email else '❌'}")
    print(f"🔐 LinkedIn Password: {'✅' if linkedin_password else '❌'}")
    print(f"🤖 Gemini API Key: {'✅' if gemini_api_key else '❌'}")
    
    if not all([linkedin_email, linkedin_password, gemini_api_key]):
        print("❌ Missing required environment variables")
        return
    
    agent = None
    try:
        # Test import
        from backend.services.autoagent_linkedin import AutoAgentLinkedIn, run_autoagent
        print("✅ Successfully imported AutoAgent LinkedIn service")
        
        # Create a test agent
        agent = AutoAgentLinkedIn()
        print("✅ AutoAgent instance created")
        
        # Test browser initialization
        print("🤖 Testing browser initialization...")
        success = await agent.initialize_browser(headless=True)
        
        if success:
            print("✅ Browser initialized successfully")
            
            # Test LinkedIn login
            print("🔐 Testing LinkedIn login...")
            login_success = await agent.login_to_linkedin()
            
            if login_success:
                print("✅ LinkedIn login successful!")
                print("🎉 All core components are working!")
            else:
                print("❌ LinkedIn login failed")
            
        else:
            print("❌ Browser initialization failed")
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Try installing missing dependencies:")
        print("   pip install PyMuPDF sentence-transformers")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        try:
            if agent is not None and hasattr(agent, 'browser') and agent.browser:
                await agent.close_browser()
        except:
            pass

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(test_run_agent())