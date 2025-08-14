"""Test configuration and basic functionality."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import os

from src.core.config import get_settings
from src.core.logging import setup_logging
from src.models import JobPosting, ResumeData, JobSearchFilters
from src.services import ResumeParser, JobMatchingService


class TestConfiguration:
    """Test configuration management."""
    
    def test_settings_load(self):
        """Test settings loading."""
        settings = get_settings()
        assert settings.app_name == "AutoAgentHire"
        assert settings.app_version == "1.0.0"
    
    def test_logging_setup(self):
        """Test logging setup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('src.core.config.get_settings') as mock_settings:
                mock_settings.return_value.logs_path = tmpdir
                mock_settings.return_value.log_level = "INFO"
                
                # Should not raise any exceptions
                setup_logging()


class TestModels:
    """Test data models."""
    
    def test_job_posting_creation(self):
        """Test JobPosting model creation."""
        job = JobPosting(
            job_id="123",
            title="Python Developer",
            company="Tech Corp",
            location="Remote",
            description="Great Python job",
            url="https://linkedin.com/jobs/123"
        )
        
        assert job.job_id == "123"
        assert job.title == "Python Developer"
        assert job.company == "Tech Corp"
    
    def test_resume_data_creation(self):
        """Test ResumeData model creation."""
        resume = ResumeData(
            file_path="/path/to/resume.pdf",
            name="John Doe",
            email="john@example.com",
            skills=["Python", "Machine Learning"],
            experience=[{"title": "Developer", "company": "Tech Corp"}]
        )
        
        assert resume.name == "John Doe"
        assert resume.email == "john@example.com"
        assert len(resume.skills) == 2
    
    def test_job_search_filters(self):
        """Test JobSearchFilters model."""
        filters = JobSearchFilters(
            keywords="Python Developer",
            location="San Francisco",
            max_results=50
        )
        
        assert filters.keywords == "Python Developer"
        assert filters.location == "San Francisco"
        assert filters.max_results == 50


class TestResumeParser:
    """Test resume parser functionality."""
    
    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = ResumeParser()
        assert parser is not None
    
    def test_text_cleaning(self):
        """Test text cleaning utility."""
        parser = ResumeParser()
        
        # Test private method if available
        if hasattr(parser, '_extract_name'):
            # Mock some functionality
            pass


class TestJobMatching:
    """Test job matching service."""
    
    def test_service_initialization(self):
        """Test service can be initialized."""
        with patch('src.services.job_matching.SentenceTransformer'):
            service = JobMatchingService()
            assert service is not None
    
    def test_index_stats(self):
        """Test getting index statistics."""
        with patch('src.services.job_matching.SentenceTransformer'):
            service = JobMatchingService()
            stats = service.get_index_stats()
            
            assert 'total_jobs' in stats
            assert 'dimension' in stats
            assert 'model_name' in stats


class TestUtilities:
    """Test utility functions."""
    
    def test_utility_imports(self):
        """Test that utilities can be imported."""
        from src.utils import (
            clean_text, extract_keywords, calculate_text_similarity,
            validate_email, validate_phone
        )
        
        # Test text cleaning
        cleaned = clean_text("  Hello   world!  ")
        assert cleaned == "Hello world!"
        
        # Test email validation
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
        
        # Test phone validation
        assert validate_phone("(555) 123-4567") == True
        assert validate_phone("invalid") == False


if __name__ == "__main__":
    pytest.main([__file__])