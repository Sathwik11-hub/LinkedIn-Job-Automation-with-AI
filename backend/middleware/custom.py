"""
Middleware for FastAPI application.

This module contains custom middleware for request/response processing,
logging, authentication, rate limiting, etc.
"""
from typing import Callable
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    
    Logs request details, response status, and processing time.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log details.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
            
        Returns:
            HTTP response
        """
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request started: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"status={response.status_code} duration={process_time:.3f}s"
        )
        
        # Add custom header with processing time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for global error handling.
    
    Catches unhandled exceptions and returns appropriate error responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with error handling.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
            
        Returns:
            HTTP response
        """
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(
                f"Unhandled exception: {str(e)} "
                f"for {request.method} {request.url.path}",
                exc_info=True
            )
            # In production, return a generic error message
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "error_type": type(e).__name__
                }
            )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding security headers to responses.
    
    Adds headers like X-Content-Type-Options, X-Frame-Options, etc.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and add security headers.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
            
        Returns:
            HTTP response with security headers
        """
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for basic rate limiting.
    
    Tracks request counts per client and enforces limits.
    Note: In production, use Redis-based rate limiting.
    """
    
    def __init__(self, app: ASGIApp, max_requests: int = 100, window_seconds: int = 60):
        """
        Initialize rate limit middleware.
        
        Args:
            app: ASGI application
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds
        """
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict = {}  # In production, use Redis
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with rate limiting.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware in chain
            
        Returns:
            HTTP response or 429 Too Many Requests
        """
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        self.requests = {
            ip: reqs for ip, reqs in self.requests.items()
            if any(t > current_time - self.window_seconds for t in reqs)
        }
        
        # Check rate limit
        if client_ip in self.requests:
            recent_requests = [
                t for t in self.requests[client_ip]
                if t > current_time - self.window_seconds
            ]
            if len(recent_requests) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"}
                )
            self.requests[client_ip] = recent_requests + [current_time]
        else:
            self.requests[client_ip] = [current_time]
        
        return await call_next(request)


class CORSMiddleware:
    """
    Note: FastAPI has built-in CORSMiddleware.
    This is a placeholder for custom CORS logic if needed.
    """
    pass
