"""
Pytest configuration and fixtures.
"""
import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# from backend.main import app
# from backend.database.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    # from backend.main import app
    # return TestClient(app)
    pass


@pytest.fixture
async def db_session():
    """Create a test database session."""
    # TODO: Implement test database session
    pass


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_job_data():
    """Sample job listing data for testing."""
    return {
        "title": "Senior Python Developer",
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "description": "We are looking for an experienced Python developer...",
        "requirements": "5+ years of Python, Django, FastAPI experience",
        "salary_min": 120000,
        "salary_max": 180000,
        "job_type": "Full-time",
        "experience_level": "Senior",
        "url": "https://example.com/job/12345"
    }


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing."""
    return {
        "contact": {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1-555-123-4567"
        },
        "skills": ["Python", "FastAPI", "Docker", "PostgreSQL"],
        "experience": [
            {
                "company": "Tech Company",
                "role": "Python Developer",
                "duration": "2020-2023"
            }
        ],
        "education": [
            {
                "degree": "BS Computer Science",
                "institution": "University",
                "year": "2020"
            }
        ]
    }
