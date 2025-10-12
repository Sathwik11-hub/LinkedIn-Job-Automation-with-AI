#!/usr/bin/env python3
"""
Validate AutoAgentHire project structure.
Checks that all required files and directories exist.
"""
import os
import sys
from pathlib import Path


def validate_structure():
    """Validate the project structure."""
    
    # Get project root - either from script location or current directory
    script_path = Path(__file__).resolve()
    if script_path.parent.name == 'scripts':
        project_root = script_path.parent.parent
    else:
        project_root = Path.cwd()
    
    print(f"📂 Project root: {project_root}\n")
    
    errors = []
    warnings = []
    
    # Required directories
    required_dirs = [
        'backend/agents',
        'backend/api',
        'backend/automation',
        'backend/database',
        'backend/llm',
        'backend/parsers',
        'backend/rag',
        'backend/matching',
        'backend/utils',
        'backend/security',
        'backend/scheduler',
        'frontend/streamlit',
        'tests/unit',
        'tests/integration',
        'tests/e2e',
        'data/resumes',
        'data/job_listings',
        'data/logs',
        'data/templates',
        'database/migrations',
        'docker',
        'docs',
        'scripts',
    ]
    
    # Required files
    required_files = [
        'README.md',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'LICENSE',
        'backend/main.py',
        'backend/config.py',
        'backend/database/models.py',
        'backend/database/schemas.py',
        'frontend/streamlit/app.py',
        'docker/docker-compose.yml',
        'docker/Dockerfile.backend',
        'docker/Dockerfile.frontend',
    ]
    
    # Optional but recommended files
    optional_files = [
        '.env',
        'CONTRIBUTING.md',
        'docs/API.md',
        'docs/ARCHITECTURE.md',
        'docs/DEPLOYMENT.md',
        'docs/USER_GUIDE.md',
    ]
    
    print("🔍 Validating AutoAgentHire project structure...\n")
    
    # Check directories
    print("📁 Checking directories...")
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} (missing)")
            errors.append(f"Missing directory: {dir_path}")
    
    print()
    
    # Check required files
    print("📄 Checking required files...")
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.is_file():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing)")
            errors.append(f"Missing file: {file_path}")
    
    print()
    
    # Check optional files
    print("📋 Checking optional files...")
    for file_path in optional_files:
        full_path = project_root / file_path
        if full_path.is_file():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ⚠ {file_path} (recommended)")
            warnings.append(f"Missing optional file: {file_path}")
    
    print()
    
    # Summary
    print("=" * 60)
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} error(s):\n")
        for error in errors:
            print(f"  • {error}")
        return False
    else:
        print("\n✅ All required files and directories exist!")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} optional file(s) missing:")
            for warning in warnings:
                print(f"  • {warning}")
        
        print("\n🎉 Project structure is valid!")
        return True


if __name__ == "__main__":
    success = validate_structure()
    sys.exit(0 if success else 1)
