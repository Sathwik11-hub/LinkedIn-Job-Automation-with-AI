"""
Configuration management for AutoAgentHire
Environment variables and application settings
"""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # FastAPI settings
    app_name: str = "AutoAgentHire"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # LinkedIn credentials
    linkedin_email: Optional[str] = None
    linkedin_password: Optional[str] = None
    
    # OpenAI/LLM settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Database settings
    database_url: str = "sqlite:///./jobs.db"
    
    # Vector store settings
    vector_store_path: str = "./vector_store"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Automation settings
    headless_browser: bool = True
    automation_delay: float = 2.0
    max_applications_per_day: int = 50
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "autoagenthire.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()