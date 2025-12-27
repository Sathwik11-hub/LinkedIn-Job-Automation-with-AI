"""
Application configuration settings.

This file can contain additional configuration logic that extends
the main config.py in the backend directory.
"""
from typing import Dict, Any


# Agent configuration
AGENT_CONFIG = {
    "job_search_agent": {
        "max_results": 100,
        "search_delay_seconds": 2,
        "platforms": ["linkedin", "indeed", "glassdoor"],
    },
    "analysis_agent": {
        "match_threshold": 0.7,
        "use_embeddings": True,
        "embedding_model": "text-embedding-3-small",
    },
    "application_agent": {
        "auto_apply_threshold": 0.85,
        "require_human_review": True,
        "max_applications_per_day": 10,
    },
}

# LLM configuration
LLM_CONFIG = {
    "openai": {
        "model": "gpt-4-turbo-preview",
        "temperature": 0.7,
        "max_tokens": 4000,
    },
    "anthropic": {
        "model": "claude-3-opus-20240229",
        "temperature": 0.7,
        "max_tokens": 4000,
    },
}

# Vector database configuration
VECTOR_DB_CONFIG = {
    "chromadb": {
        "host": "localhost",
        "port": 8001,
        "collection_name": "job_embeddings",
    },
    "pinecone": {
        "index_name": "autoagenthire",
        "dimension": 1536,
        "metric": "cosine",
    },
}

# Workflow configuration
WORKFLOW_CONFIG = {
    "job_search": {
        "steps": ["search", "parse", "filter", "rank"],
        "timeout_seconds": 300,
    },
    "application": {
        "steps": ["match", "generate_cover_letter", "fill_form", "submit"],
        "timeout_seconds": 600,
    },
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "data/logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}


def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for a specific agent."""
    return AGENT_CONFIG.get(agent_name, {})


def get_llm_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a specific LLM provider."""
    return LLM_CONFIG.get(provider, {})


def get_vector_db_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a specific vector database provider."""
    return VECTOR_DB_CONFIG.get(provider, {})
