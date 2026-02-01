"""
Authentication middleware for FastAPI.

Provides:
- JWT token validation
- User authentication for protected endpoints
- Optional authentication for public endpoints
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.auth import get_auth_service, AuthService


security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[dict]:
    """
    Get current authenticated user from JWT token.
    Returns None if no token or invalid token (for optional auth).
    
    Args:
        credentials: Bearer token from Authorization header
        auth_service: Authentication service
        
    Returns:
        User data dict or None
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    user_data = auth_service.verify_session_token(token)
    
    return user_data


async def require_auth(
    current_user: Optional[dict] = Depends(get_current_user)
) -> dict:
    """
    Require authentication for endpoint.
    Raises 401 if not authenticated.
    
    Args:
        current_user: Current user from token
        
    Returns:
        User data dict
        
    Raises:
        HTTPException: 401 if not authenticated
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return current_user


async def optional_auth(
    current_user: Optional[dict] = Depends(get_current_user)
) -> Optional[dict]:
    """
    Optional authentication for endpoint.
    Returns user if authenticated, None otherwise.
    
    Args:
        current_user: Current user from token
        
    Returns:
        User data dict or None
    """
    return current_user


async def get_user_id(
    current_user: dict = Depends(require_auth)
) -> int:
    """
    Get current user's ID.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User ID
    """
    return current_user["user_id"]


async def get_user_email(
    current_user: dict = Depends(require_auth)
) -> str:
    """
    Get current user's email.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User email
    """
    return current_user["email"]
