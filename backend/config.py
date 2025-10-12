"""
Configuration management using Pydantic Settings.
Loads environment variables and provides type-safe configuration.
"""
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "AutoAgentHire"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./autoagenthire.db"  # Default to SQLite for demo
    SYNC_DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Vector Database
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_PERSIST_DIRECTORY: str = "./vector_db/data"
    
    # Pinecone (alternative)
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: str = "demo-key-replace-with-real-key"
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.7
    
    # Anthropic (alternative)
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # CrewAI
    CREWAI_TELEMETRY: bool = False
    
    # OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    
    LINKEDIN_OAUTH_CLIENT_ID: Optional[str] = None
    LINKEDIN_OAUTH_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_OAUTH_REDIRECT_URI: Optional[str] = None
    
    # Web Automation
    SELENIUM_HEADLESS: bool = True
    SELENIUM_IMPLICIT_WAIT: int = 10
    PLAYWRIGHT_HEADLESS: bool = True
    PLAYWRIGHT_TIMEOUT: int = 30000
    
    # Proxy
    USE_PROXY: bool = False
    PROXY_URL: Optional[str] = None
    
    # Email
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: Optional[str] = None
    NOTIFICATION_EMAIL: Optional[str] = None
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Job Search
    MAX_JOBS_PER_SEARCH: int = 100
    SEARCH_DELAY_SECONDS: int = 2
    MAX_APPLICATIONS_PER_DAY: int = 10
    
    # Feature Flags
    ENABLE_AUTO_APPLY: bool = False
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_DAILY_REPORTS: bool = True
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Encryption
    ENCRYPTION_KEY: Optional[str] = None
    
    # Frontend
    STREAMLIT_PORT: int = 8501
    REACT_APP_API_URL: str = "http://localhost:8000"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8501"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_RESUME_EXTENSIONS: str = "pdf,docx,txt"
    
    def get_allowed_extensions(self) -> List[str]:
        """Parse allowed extensions from string."""
        return [ext.strip() for ext in self.ALLOWED_RESUME_EXTENSIONS.split(",")]
    
    # LinkedIn Automation
    LINKEDIN_EMAIL: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    
    # Alternative LLM: Local Llama
    LLAMA_MODEL_PATH: Optional[str] = None
    
    # Logging
    LOG_FILE_PATH: str = "data/logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "30 days"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env


# Global settings instance
settings = Settings()
