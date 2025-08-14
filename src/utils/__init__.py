"""Utility functions for AutoAgentHire."""

import re
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\(\)]', '', text)
    
    return text.strip()


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text."""
    if not text:
        return []
    
    # Convert to lowercase and split
    words = clean_text(text.lower()).split()
    
    # Filter out common stop words and short words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    keywords = []
    for word in words:
        # Remove punctuation
        word = re.sub(r'[^\w]', '', word)
        
        if (len(word) >= min_length and 
            word not in stop_words and 
            not word.isdigit()):
            keywords.append(word)
    
    return list(set(keywords))  # Remove duplicates


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using simple word overlap."""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


def generate_hash(text: str) -> str:
    """Generate MD5 hash of text."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def save_json(data: Any, file_path: str) -> bool:
    """Save data to JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception:
        return False


def load_json(file_path: str) -> Optional[Any]:
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def format_date(date_obj: datetime) -> str:
    """Format datetime object to string."""
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def parse_date(date_string: str) -> Optional[datetime]:
    """Parse date string to datetime object."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits) <= 15


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system operations."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename


def create_backup_filename(original_path: str) -> str:
    """Create backup filename with timestamp."""
    path = Path(original_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return str(path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}")


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """Retry operation with exponential backoff."""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))


def is_url_valid(url: str) -> bool:
    """Check if URL is valid."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def ensure_directory(path: str) -> bool:
    """Ensure directory exists."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


class ProgressTracker:
    """Simple progress tracker for long operations."""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, increment: int = 1):
        """Update progress."""
        self.current += increment
        
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress status."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        percentage = (self.current / self.total * 100) if self.total > 0 else 0
        
        return {
            "description": self.description,
            "current": self.current,
            "total": self.total,
            "percentage": round(percentage, 1),
            "elapsed_seconds": round(elapsed, 1)
        }
    
    def is_complete(self) -> bool:
        """Check if progress is complete."""
        return self.current >= self.total