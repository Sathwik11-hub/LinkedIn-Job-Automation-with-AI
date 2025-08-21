"""
Logging utility for AutoAgentHire
Centralized logging configuration
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from app.config import settings


def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with consistent formatting
    
    Args:
        name: Logger name (usually __name__)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file_path = log_file or settings.log_file
    if log_file_path:
        try:
            # Ensure log directory exists
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger


class StructuredLogger:
    """
    Structured logger for better log analysis
    """
    
    def __init__(self, name: str):
        self.logger = setup_logger(name)
    
    def log_job_search(self, keywords: str, location: str, count: int):
        """Log job search event"""
        self.logger.info(
            f"JOB_SEARCH | keywords={keywords} | location={location} | count={count}"
        )
    
    def log_job_application(self, job_id: str, company: str, title: str, success: bool):
        """Log job application event"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"JOB_APPLICATION | job_id={job_id} | company={company} | title={title} | status={status}"
        )
    
    def log_automation_step(self, step: str, action: str, success: bool, details: str = ""):
        """Log automation step"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"AUTOMATION_STEP | step={step} | action={action} | status={status} | details={details}"
        )
    
    def log_ai_operation(self, operation: str, model: str, input_size: int, output_size: int, duration: float):
        """Log AI/ML operation"""
        self.logger.info(
            f"AI_OPERATION | operation={operation} | model={model} | input_size={input_size} | output_size={output_size} | duration={duration:.2f}s"
        )
    
    def log_error(self, operation: str, error: Exception, context: dict = None):
        """Log error with context"""
        context_str = " | ".join([f"{k}={v}" for k, v in (context or {}).items()])
        self.logger.error(
            f"ERROR | operation={operation} | error={str(error)} | context={context_str}"
        )


# Global logger instances
main_logger = setup_logger("autoagenthire")
structured_logger = StructuredLogger("autoagenthire.structured")


def log_performance(func):
    """
    Decorator to log function performance
    """
    import functools
    import time
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = setup_logger(func.__module__)
        
        try:
            logger.debug(f"Starting {func.__name__}")
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Completed {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error in {func.__name__} after {duration:.2f}s: {str(e)}")
            raise
    
    return wrapper


def log_async_performance(func):
    """
    Decorator to log async function performance
    """
    import functools
    import time
    import asyncio
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        logger = setup_logger(func.__module__)
        
        try:
            logger.debug(f"Starting {func.__name__}")
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Completed {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error in {func.__name__} after {duration:.2f}s: {str(e)}")
            raise
    
    return wrapper