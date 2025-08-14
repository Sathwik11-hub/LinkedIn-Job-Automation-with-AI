"""Logging configuration for AutoAgentHire."""

import sys
from pathlib import Path
from typing import Dict, Any

from loguru import logger

from .config import get_settings


def setup_logging() -> None:
    """Configure logging for the application."""
    settings = get_settings()
    
    # Remove default handler
    logger.remove()
    
    # Console logging
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # File logging
    log_file = Path(settings.logs_path) / "autoagenthire.log"
    logger.add(
        log_file,
        format=log_format,
        level=settings.log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # Error file logging
    error_log_file = Path(settings.logs_path) / "errors.log"
    logger.add(
        error_log_file,
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info(f"Logging configured - Level: {settings.log_level}")


def get_logger(name: str = None):
    """Get a logger instance."""
    if name:
        return logger.bind(name=name)
    return logger


class LoggerMixin:
    """Mixin to add logging to classes."""
    
    @property
    def logger(self):
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)