"""Test fixtures and configuration for pytest."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch

@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_settings():
    """Mock application settings."""
    with patch('src.core.config.get_settings') as mock:
        mock.return_value.app_name = "AutoAgentHire"
        mock.return_value.app_version = "1.0.0"
        mock.return_value.debug = True
        mock.return_value.log_level = "INFO"
        mock.return_value.linkedin_email = "test@example.com"
        mock.return_value.linkedin_password = "testpass"
        mock.return_value.openai_api_key = "test-key"
        mock.return_value.resume_path = "./data/resumes/"
        mock.return_value.logs_path = "./logs/"
        mock.return_value.jobs_data_path = "./data/jobs/"
        mock.return_value.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        mock.return_value.vector_db_type = "faiss"
        mock.return_value.max_applications_per_day = 50
        mock.return_value.application_delay_seconds = 30
        yield mock.return_value


@pytest.fixture
def sample_job_posting():
    """Sample job posting for tests."""
    from src.models import JobPosting
    
    return JobPosting(
        job_id="123456",
        title="Senior Python Developer",
        company="TechCorp Inc",
        location="San Francisco, CA",
        description="We are looking for a Senior Python Developer with experience in web development, machine learning, and cloud technologies. The ideal candidate will have 5+ years of experience with Python, Django, Flask, AWS, and Docker.",
        requirements="Python, Django, Flask, AWS, Docker, Machine Learning",
        url="https://linkedin.com/jobs/123456"
    )


@pytest.fixture
def sample_resume_data():
    """Sample resume data for tests."""
    from src.models import ResumeData
    
    return ResumeData(
        file_path="/path/to/resume.pdf",
        name="John Doe",
        email="john.doe@example.com",
        phone="(555) 123-4567",
        skills=["Python", "Django", "Flask", "Machine Learning", "AWS", "Docker"],
        experience=[
            {
                "title": "Senior Software Engineer",
                "company": "Tech Solutions Inc",
                "period": "2020-2023",
                "description": "Developed web applications using Python and Django"
            },
            {
                "title": "Software Developer",
                "company": "StartupCorp",
                "period": "2018-2020", 
                "description": "Built microservices using Flask and deployed on AWS"
            }
        ],
        education=[
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "University of Technology",
                "year": "2018"
            }
        ],
        summary="Experienced Python developer with expertise in web development and machine learning"
    )