#!/usr/bin/env python3
"""
Quick test script to verify AutoAgentHire components
"""

import sys
import os
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test that all major components can be imported"""
    print("🧪 Testing component imports...")
    
    try:
        # Test core components
        from app.core.config import settings
        print("✅ Core config imported")
        
        from app.models.user import User
        from app.models.job import Job
        from app.models.application import Application
        print("✅ Database models imported")
        
        from app.services.ai.llm_service import LLMService
        from app.services.ai.resume_parser import ResumeParser
        from app.services.ai.rag_service import RAGService
        from app.services.ai.job_matcher import JobMatcher
        print("✅ AI services imported")
        
        from app.services.automation.linkedin_bot import LinkedInBot
        from app.services.automation.form_filler import FormFiller
        print("✅ Automation services imported")
        
        from app.utils.helpers import validate_email, extract_skills_from_text
        from app.utils.exceptions import AutoAgentHireException
        print("✅ Utility modules imported")
        
        print("🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        # Test resume parser
        from app.services.ai.resume_parser import ResumeParser
        parser = ResumeParser()
        result = parser.parse_resume("I have experience with Python and JavaScript.")
        assert isinstance(result, dict)
        assert "skills" in result
        print("✅ Resume parser basic test passed")
        
        # Test utility functions
        from app.utils.helpers import validate_email, extract_skills_from_text
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        
        skills = extract_skills_from_text("I work with Python, React, and AWS")
        assert isinstance(skills, list)
        print("✅ Utility functions test passed")
        
        # Test config
        from app.core.config import settings
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'openai_api_key')
        print("✅ Configuration test passed")
        
        print("🎉 All functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "backend/app/main.py",
        "backend/requirements.txt",
        "frontend/package.json",
        "frontend/src/App.tsx",
        "docker-compose.yml",
        ".env.example",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests"""
    print("🚀 AutoAgentHire Component Test Suite")
    print("=" * 40)
    
    # Change to project root
    os.chdir(Path(__file__).parent.parent)
    
    tests = [
        test_file_structure,
        test_imports,
        test_basic_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoAgentHire is ready for development.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())