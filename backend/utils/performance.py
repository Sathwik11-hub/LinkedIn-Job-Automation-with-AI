"""
Performance optimization utilities for AutoAgentHire system.

This module provides:
- Caching layer for resumes and job listings
- Parallel processing helpers
- Performance monitoring
"""
import asyncio
import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable, TypeVar
from functools import wraps

T = TypeVar('T')


class CacheManager:
    """
    In-memory cache with TTL support for resumes and job listings.
    Reduces redundant parsing and API calls.
    """
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
    
    def _get_key(self, namespace: str, identifier: str) -> str:
        """Generate cache key from namespace and identifier."""
        return f"{namespace}:{identifier}"
    
    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry has expired."""
        if 'expires_at' not in cache_entry:
            return True
        return datetime.now() > cache_entry['expires_at']
    
    def get(self, namespace: str, identifier: str) -> Optional[Any]:
        """
        Retrieve cached value.
        
        Args:
            namespace: Cache namespace (e.g., 'resume', 'job')
            identifier: Unique identifier (e.g., file path, job URL)
            
        Returns:
            Cached value or None if not found/expired
        """
        key = self._get_key(namespace, identifier)
        
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        if self._is_expired(entry):
            del self._cache[key]
            return None
        
        return entry['value']
    
    def set(
        self,
        namespace: str,
        identifier: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> None:
        """
        Store value in cache.
        
        Args:
            namespace: Cache namespace
            identifier: Unique identifier
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        key = self._get_key(namespace, identifier)
        ttl = ttl if ttl is not None else self.default_ttl
        
        self._cache[key] = {
            'value': value,
            'expires_at': datetime.now() + timedelta(seconds=ttl),
            'created_at': datetime.now()
        }
    
    def invalidate(self, namespace: str, identifier: str) -> None:
        """Remove entry from cache."""
        key = self._get_key(namespace, identifier)
        if key in self._cache:
            del self._cache[key]
    
    def clear(self, namespace: Optional[str] = None) -> None:
        """
        Clear cache entries.
        
        Args:
            namespace: If provided, only clear entries in this namespace
        """
        if namespace is None:
            self._cache.clear()
        else:
            keys_to_delete = [
                key for key in self._cache.keys()
                if key.startswith(f"{namespace}:")
            ]
            for key in keys_to_delete:
                del self._cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self._cache)
        expired_entries = sum(
            1 for entry in self._cache.values()
            if self._is_expired(entry)
        )
        
        return {
            'total_entries': total_entries,
            'active_entries': total_entries - expired_entries,
            'expired_entries': expired_entries
        }


def cached(
    cache_manager: CacheManager,
    namespace: str,
    ttl: Optional[int] = None,
    key_func: Optional[Callable] = None
):
    """
    Decorator to cache function results.
    
    Args:
        cache_manager: CacheManager instance
        namespace: Cache namespace
        ttl: Time-to-live override
        key_func: Optional function to generate cache key from args
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: use stringified args
                cache_key = hashlib.md5(
                    json.dumps([str(args), str(kwargs)], sort_keys=True).encode()
                ).hexdigest()
            
            # Check cache
            cached_value = cache_manager.get(namespace, cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            cache_manager.set(namespace, cache_key, result, ttl)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = hashlib.md5(
                    json.dumps([str(args), str(kwargs)], sort_keys=True).encode()
                ).hexdigest()
            
            # Check cache
            cached_value = cache_manager.get(namespace, cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(namespace, cache_key, result, ttl)
            return result
        
        # Return appropriate wrapper
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class ParallelProcessor:
    """
    Utility for processing tasks in parallel with concurrency control.
    """
    
    def __init__(self, max_concurrent: int = 5):
        """
        Initialize parallel processor.
        
        Args:
            max_concurrent: Maximum number of concurrent tasks
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_batch(
        self,
        items: List[Any],
        process_func: Callable,
        *args,
        **kwargs
    ) -> List[Any]:
        """
        Process items in parallel with concurrency control.
        
        Args:
            items: List of items to process
            process_func: Async function to process each item
            *args, **kwargs: Additional arguments for process_func
            
        Returns:
            List of results in same order as input items
        """
        async def process_with_semaphore(item):
            async with self.semaphore:
                try:
                    return await process_func(item, *args, **kwargs)
                except Exception as e:
                    print(f"⚠️  Error processing item: {str(e)}")
                    return None
        
        # Create tasks for all items
        tasks = [process_with_semaphore(item) for item in items]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None values
        return [r for r in results if r is not None and not isinstance(r, Exception)]


class PerformanceMonitor:
    """
    Monitor and track performance metrics.
    """
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
    
    def track(self, name: str):
        """
        Decorator to track function execution time.
        
        Args:
            name: Metric name
        """
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self._record_metric(name, duration)
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self._record_metric(name, duration)
            
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def _record_metric(self, name: str, value: float) -> None:
        """Record a metric value."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """
        Get statistics for a metric.
        
        Args:
            name: Metric name
            
        Returns:
            Dictionary with min, max, avg, total, count
        """
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        values = self.metrics[name]
        return {
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'total': sum(values),
            'count': len(values)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all tracked metrics."""
        return {
            name: self.get_stats(name)
            for name in self.metrics.keys()
        }
    
    def clear(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()


# Global instances
_cache_manager = CacheManager(default_ttl=3600)
_performance_monitor = PerformanceMonitor()


def get_cache_manager() -> CacheManager:
    """Get global cache manager instance."""
    return _cache_manager


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance."""
    return _performance_monitor
