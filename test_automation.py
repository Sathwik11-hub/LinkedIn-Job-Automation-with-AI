#!/usr/bin/env python3
"""
Test automation script to verify LinkedIn bot works.
"""
import asyncio
from backend.agents.linkedin_bot import LinkedInBot


async def test_bot():
    """Test the LinkedIn bot with async API."""
    print("🤖 Testing LinkedIn Bot...")
    
    # Create bot instance
    bot = LinkedInBot(
        email="test@example.com",  # Replace with your email
        password="test123",  # Replace with your password
        headless=True
    )
    
    try:
        print("✓ Bot created successfully")
        
        # Test starting the browser
        await bot.start()
        print("✓ Browser started successfully")
        
        # Test stopping the browser
        await bot.stop()
        print("✓ Browser stopped successfully")
        
        print("\n✅ All tests passed!")
        print("The bot is working correctly with async Playwright API")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        
        
if __name__ == "__main__":
    asyncio.run(test_bot())
