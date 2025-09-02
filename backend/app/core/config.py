import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/autoagenthire"
    redis_url: str = "redis://localhost:6379"
    
    # AI Services
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Security
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LinkedIn Credentials
    linkedin_email: str = ""
    linkedin_password: str = ""
    
    # Application
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"
    
    # Browser Automation
    headless_browser: bool = True
    browser_timeout: int = 30000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()