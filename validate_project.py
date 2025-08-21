#!/usr/bin/env python3
"""
Basic validation script for AutoAgentHire project structure
This script validates that all modules can be imported and basic structure is correct
"""

import sys
import os
from pathlib import Path

def test_project_structure():
    """Test that all required files and directories exist"""
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/config.py',
        'app/models/__init__.py',
        'app/models/job_schema.py',
        'app/routes/__init__.py',
        'app/routes/jobs.py',
        'app/services/__init__.py',
        'app/services/job_scraper.py',
        'app/services/resume_parser.py',
        'app/services/matcher.py',
        'app/services/cover_letter_generator.py',
        'app/services/auto_apply.py',
        'app/utils/__init__.py',
        'app/utils/logger.py',
        'app/utils/vectorstore.py',
        'automation/__init__.py',
        'automation/linkedin_bot.py',
        'requirements.txt',
        'run.sh',
        '.env.example',
        '.gitignore',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_module_imports():
    """Test that key modules can be imported without dependency errors"""
    print("\n🧪 Testing module imports...")
    
    # Test basic Python imports (no external dependencies)
    try:
        from app.config import Settings
        print("✅ app.config imported successfully")
    except ImportError as e:
        print(f"❌ app.config import failed: {e}")
        return False
    
    try:
        from app.models.job_schema import Job, JobSearchRequest
        print("✅ app.models.job_schema imported successfully")
    except ImportError as e:
        print(f"❌ app.models.job_schema import failed: {e}")
        return False
    
    return True

def test_requirements_file():
    """Test that requirements.txt is properly formatted"""
    print("\n📦 Testing requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Filter out comments and empty lines
        packages = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
        
        if len(packages) < 10:
            print(f"❌ Too few packages in requirements.txt ({len(packages)})")
            return False
        
        # Check for key packages
        key_packages = ['fastapi', 'selenium', 'pydantic']
        found_packages = []
        
        for package in packages:
            package_name = package.split('==')[0].split('>=')[0].split('[')[0]
            if package_name in key_packages:
                found_packages.append(package_name)
        
        if len(found_packages) == len(key_packages):
            print(f"✅ requirements.txt contains {len(packages)} packages including key dependencies")
            return True
        else:
            missing = set(key_packages) - set(found_packages)
            print(f"❌ Missing key packages: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_run_script():
    """Test that run.sh script is executable and properly formatted"""
    print("\n🏃 Testing run.sh script...")
    
    run_script = Path('run.sh')
    
    if not run_script.exists():
        print("❌ run.sh does not exist")
        return False
    
    # Check if executable
    if not os.access(run_script, os.X_OK):
        print("❌ run.sh is not executable")
        return False
    
    # Check content
    with open(run_script, 'r') as f:
        content = f.read()
    
    required_content = ['#!/bin/bash', 'uvicorn', 'app.main:app']
    for item in required_content:
        if item not in content:
            print(f"❌ run.sh missing required content: {item}")
            return False
    
    print("✅ run.sh is properly configured")
    return True

def main():
    """Run all validation tests"""
    print("🔍 AutoAgentHire Project Structure Validation")
    print("=" * 50)
    
    tests = [
        test_project_structure,
        test_module_imports,
        test_requirements_file,
        test_run_script
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All validation tests passed!")
        print("✅ Project structure is correct and ready for development")
        return 0
    else:
        failed_count = len([r for r in results if not r])
        print(f"❌ {failed_count} validation test(s) failed")
        print("⚠️  Please fix the issues above before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())