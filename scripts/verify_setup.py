#!/usr/bin/env python3
"""
Setup verification script for AutoAgentHire project.

This script verifies that the project structure is correctly set up
and all necessary directories and files exist.
"""
import os
import sys
from pathlib import Path


def check_directory(path: str, description: str) -> bool:
    """Check if a directory exists."""
    if os.path.isdir(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ Missing {description}: {path}")
        return False


def check_file(path: str, description: str) -> bool:
    """Check if a file exists."""
    if os.path.isfile(path):
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ Missing {description}: {path}")
        return False


def main():
    """Main verification function."""
    print("=" * 70)
    print("AutoAgentHire Project Structure Verification")
    print("=" * 70)
    print()
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    all_checks_passed = True
    
    # Check critical directories
    print("Checking Backend Directories:")
    print("-" * 70)
    directories = [
        ("backend/agents", "Agents directory"),
        ("backend/api", "API directory"),
        ("backend/orchestration", "Orchestration directory"),
        ("backend/services", "Services directory"),
        ("backend/models", "Models directory"),
        ("backend/middleware", "Middleware directory"),
        ("backend/database", "Database directory"),
        ("backend/llm", "LLM directory"),
        ("backend/routes", "Routes directory"),
        ("backend/security", "Security directory"),
    ]
    
    for dir_path, desc in directories:
        if not check_directory(dir_path, desc):
            all_checks_passed = False
    
    print()
    print("Checking Data Directories:")
    print("-" * 70)
    data_directories = [
        ("data/logs", "Logs directory"),
        ("data/uploads", "Uploads directory"),
        ("data/resumes", "Resumes directory"),
        ("data/vector_db", "Vector DB directory"),
    ]
    
    for dir_path, desc in data_directories:
        if not check_directory(dir_path, desc):
            all_checks_passed = False
    
    print()
    print("Checking Test Directories:")
    print("-" * 70)
    test_directories = [
        ("tests/unit", "Unit tests directory"),
        ("tests/integration", "Integration tests directory"),
        ("tests/e2e", "E2E tests directory"),
    ]
    
    for dir_path, desc in test_directories:
        if not check_directory(dir_path, desc):
            all_checks_passed = False
    
    print()
    print("Checking Deployment Directories:")
    print("-" * 70)
    deployment_directories = [
        ("deployment/kubernetes", "Kubernetes directory"),
        ("alembic/versions", "Alembic versions directory"),
        ("config", "Config directory"),
    ]
    
    for dir_path, desc in deployment_directories:
        if not check_directory(dir_path, desc):
            all_checks_passed = False
    
    print()
    print("Checking Essential Files:")
    print("-" * 70)
    files = [
        ("pyproject.toml", "Project configuration"),
        ("requirements.txt", "Dependencies"),
        (".env.example", "Environment template"),
        ("alembic.ini", "Alembic configuration"),
        ("Makefile", "Make commands"),
        ("CONTRIBUTING.md", "Contributing guidelines"),
        (".dockerignore", "Docker ignore"),
        ("README.md", "README"),
        ("backend/config.py", "Backend config"),
        ("backend/main.py", "FastAPI app"),
    ]
    
    for file_path, desc in files:
        if not check_file(file_path, desc):
            all_checks_passed = False
    
    print()
    print("Checking New Module Files:")
    print("-" * 70)
    new_files = [
        ("backend/orchestration/orchestrator.py", "Orchestrator module"),
        ("backend/services/job_service.py", "Job service"),
        ("backend/models/domain.py", "Domain models"),
        ("backend/middleware/custom.py", "Custom middleware"),
        ("config/settings.py", "Config settings"),
        ("alembic/env.py", "Alembic environment"),
        ("deployment/kubernetes/backend-deployment.yaml", "K8s deployment"),
        ("tests/integration/test_integration.py", "Integration tests"),
        ("tests/e2e/test_e2e_flows.py", "E2E tests"),
        ("docs/PROJECT_STRUCTURE.md", "Project structure docs"),
    ]
    
    for file_path, desc in new_files:
        if not check_file(file_path, desc):
            all_checks_passed = False
    
    print()
    print("=" * 70)
    if all_checks_passed:
        print("✓ All checks passed! Project structure is correctly set up.")
        print("=" * 70)
        print()
        print("Next steps:")
        print("1. Copy .env.example to .env and configure your environment")
        print("2. Install dependencies: make install-dev")
        print("3. Initialize database: make db-upgrade")
        print("4. Run the application: make run-dev")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
