from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class AutoAgentHireException(Exception):
    """Base exception class for AutoAgentHire"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(AutoAgentHireException):
    """Raised when data validation fails"""
    pass

class AuthenticationError(AutoAgentHireException):
    """Raised when authentication fails"""
    pass

class AuthorizationError(AutoAgentHireException):
    """Raised when user lacks required permissions"""
    pass

class ExternalServiceError(AutoAgentHireException):
    """Raised when external service calls fail"""
    pass

class LinkedInBotError(ExternalServiceError):
    """Raised when LinkedIn automation fails"""
    pass

class AIServiceError(ExternalServiceError):
    """Raised when AI service calls fail"""
    pass

class DatabaseError(AutoAgentHireException):
    """Raised when database operations fail"""
    pass

class FileProcessingError(AutoAgentHireException):
    """Raised when file processing fails"""
    pass

# HTTP Exception handlers
def create_http_exception(
    status_code: int,
    message: str,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    """Create a standardized HTTP exception"""
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "details": details or {},
            "error_code": f"AAH_{status_code}"
        }
    )

def validation_exception(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    return create_http_exception(status.HTTP_422_UNPROCESSABLE_ENTITY, message, details)

def authentication_exception(message: str = "Authentication required") -> HTTPException:
    return create_http_exception(status.HTTP_401_UNAUTHORIZED, message)

def authorization_exception(message: str = "Insufficient permissions") -> HTTPException:
    return create_http_exception(status.HTTP_403_FORBIDDEN, message)

def not_found_exception(resource: str = "Resource") -> HTTPException:
    return create_http_exception(status.HTTP_404_NOT_FOUND, f"{resource} not found")

def internal_server_exception(message: str = "Internal server error") -> HTTPException:
    return create_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, message)

def external_service_exception(service: str, message: str) -> HTTPException:
    return create_http_exception(
        status.HTTP_503_SERVICE_UNAVAILABLE,
        f"{service} service unavailable",
        {"service": service, "error": message}
    )