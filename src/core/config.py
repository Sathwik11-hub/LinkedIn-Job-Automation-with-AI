"""Core configuration module for AutoAgentHire."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ImportError:
    from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""
    
    # App Info
    app_name: str = "AutoAgentHire"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # LinkedIn Credentials
    linkedin_email: str
    linkedin_password: str
    
    # AI API Keys
    openai_api_key: Optional[str] = None
    llama_api_url: Optional[str] = None
    llama_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./autoagenthire.db"
    
    # Job Search Settings
    default_location: str = "Remote"
    default_experience_level: str = "Mid-Senior level"
    max_applications_per_day: int = 50
    application_delay_seconds: int = 30
    
    # Vector Database
    vector_db_type: str = "faiss"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # File Paths
    resume_path: str = "./data/resumes/"
    logs_path: str = "./logs/"
    jobs_data_path: str = "./data/jobs/"
    
    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    
    @validator("resume_path", "logs_path", "jobs_data_path")
    def ensure_path_exists(cls, v):
        """Ensure directories exist."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()