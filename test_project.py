#!/usr/bin/env python3
"""Simple test script to validate the AutoAgentHire project structure."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_imports():
    """Test that basic modules can be imported."""
    print("🧪 Testing basic imports...")
    
    try:
        from src.core.config import get_settings
        print("✅ Core config import successful")
    except Exception as e:
        print(f"❌ Core config import failed: {e}")
        return False
    
    try:
        from src.core.logging import setup_logging
        print("✅ Core logging import successful") 
    except Exception as e:
        print(f"❌ Core logging import failed: {e}")
        return False
    
    try:
        from src.models import JobPosting, ResumeData, JobSearchFilters
        print("✅ Models import successful")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading."""
    print("\n🔧 Testing configuration...")
    
    # Set minimal required environment variables
    os.environ.setdefault('LINKEDIN_EMAIL', 'test@example.com')
    os.environ.setdefault('LINKEDIN_PASSWORD', 'testpass')
    os.environ.setdefault('SECRET_KEY', 'test_secret_key_change_in_production')
    
    try:
        from src.core.config import get_settings
        settings = get_settings()
        
        print(f"✅ App Name: {settings.app_name}")
        print(f"✅ App Version: {settings.app_version}")
        print(f"✅ Debug Mode: {settings.debug}")
        print(f"✅ Log Level: {settings.log_level}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_models():
    """Test data models."""
    print("\n📊 Testing data models...")
    
    try:
        from src.models import JobPosting, ResumeData, JobSearchFilters, JobExperienceLevel
        
        # Test JobPosting
        job = JobPosting(
            job_id="test123",
            title="Python Developer",
            company="Test Corp",
            location="Remote",
            description="Test job description",
            url="https://example.com/job/test123"
        )
        print(f"✅ JobPosting created: {job.title} at {job.company}")
        
        # Test ResumeData
        resume = ResumeData(
            file_path="/test/resume.pdf",
            name="Test User",
            email="test@example.com",
            skills=["Python", "FastAPI", "Machine Learning"]
        )
        print(f"✅ ResumeData created: {resume.name} with {len(resume.skills)} skills")
        
        # Test JobSearchFilters
        filters = JobSearchFilters(
            keywords="Python Developer",
            location="San Francisco",
            experience_level=JobExperienceLevel.MID_SENIOR,
            max_results=25
        )
        print(f"✅ JobSearchFilters created: {filters.keywords} in {filters.location}")
        
        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation."""
    print("\n🚀 Testing FastAPI app...")
    
    try:
        # Set environment variables
        os.environ.setdefault('LINKEDIN_EMAIL', 'test@example.com')
        os.environ.setdefault('LINKEDIN_PASSWORD', 'testpass')
        os.environ.setdefault('SECRET_KEY', 'test_secret_key')
        
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Check if app has expected attributes
        if hasattr(app, 'routes'):
            route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
            print(f"✅ Found {len(route_paths)} routes: {route_paths[:5]}...")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        return False

def test_directory_structure():
    """Test that required directories exist or can be created."""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        "src/core",
        "src/models", 
        "src/services",
        "src/utils",
        "tests",
        "data/resumes",
        "data/jobs",
        "logs"
    ]
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Directory created: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to create directory {dir_path}: {e}")
                all_good = False
    
    return all_good

def test_required_files():
    """Test that required files exist."""
    print("\n📄 Testing required files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.template",
        ".gitignore",
        "README.md",
        "src/__init__.py",
        "src/core/__init__.py",
        "src/core/config.py",
        "src/core/logging.py",
        "src/models/__init__.py",
        "src/services/__init__.py",
        "src/utils/__init__.py"
    ]
    
    all_good = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good

def main():
    """Run all tests."""
    print("🎯 AutoAgentHire Project Validation")
    print("=" * 50)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Required Files", test_required_files),
        ("Basic Imports", test_basic_imports),
        ("Configuration", test_configuration),
        ("Data Models", test_models),
        ("FastAPI App", test_fastapi_app),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoAgentHire project structure is valid.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)