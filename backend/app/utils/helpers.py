from typing import Dict, Any, List, Optional
import re
import json
from datetime import datetime, timedelta

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digits
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15

def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format"""
    pattern = r'https?://(www\.)?linkedin\.com/in/[\w-]+'
    return re.match(pattern, url) is not None

def sanitize_text(text: str, max_length: int = None) -> str:
    """Sanitize text input"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text

def extract_salary_range(text: str) -> Dict[str, Optional[float]]:
    """Extract salary range from text"""
    # Common salary patterns
    patterns = [
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*-\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d{1,3}(?:,\d{3})*)\s*-\s*(\d{1,3}(?:,\d{3})*)\s*(?:k|thousand)',
        r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'(\d{1,3}(?:,\d{3})*)\s*(?:k|thousand)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                # Range found
                min_sal = float(match.group(1).replace(',', ''))
                max_sal = float(match.group(2).replace(',', ''))
                
                # Convert K to thousands
                if 'k' in text.lower() or 'thousand' in text.lower():
                    min_sal *= 1000
                    max_sal *= 1000
                
                return {"min": min_sal, "max": max_sal}
            else:
                # Single value found
                salary = float(match.group(1).replace(',', ''))
                if 'k' in text.lower() or 'thousand' in text.lower():
                    salary *= 1000
                
                return {"min": salary, "max": None}
    
    return {"min": None, "max": None}

def parse_job_posting_date(date_text: str) -> Optional[datetime]:
    """Parse job posting date from various formats"""
    now = datetime.now()
    
    # Handle relative dates
    if 'today' in date_text.lower():
        return now
    elif 'yesterday' in date_text.lower():
        return now - timedelta(days=1)
    elif 'week' in date_text.lower():
        weeks = re.search(r'(\d+)\s*week', date_text)
        if weeks:
            return now - timedelta(weeks=int(weeks.group(1)))
        return now - timedelta(weeks=1)
    elif 'month' in date_text.lower():
        months = re.search(r'(\d+)\s*month', date_text)
        if months:
            return now - timedelta(days=int(months.group(1)) * 30)
        return now - timedelta(days=30)
    elif 'day' in date_text.lower():
        days = re.search(r'(\d+)\s*day', date_text)
        if days:
            return now - timedelta(days=int(days.group(1)))
        return now - timedelta(days=1)
    
    # Try to parse absolute dates
    date_formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%B %d, %Y',
        '%b %d, %Y',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_text, fmt)
        except ValueError:
            continue
    
    return None

def extract_company_size(text: str) -> Optional[str]:
    """Extract company size category from text"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['startup', '1-10', '1-50', 'small startup']):
        return 'startup'
    elif any(word in text_lower for word in ['51-200', '50-200', 'small', 'small company']):
        return 'small'
    elif any(word in text_lower for word in ['201-1000', '200-1000', 'medium', 'mid-size']):
        return 'medium'
    elif any(word in text_lower for word in ['1000+', '1000', 'large', 'enterprise', 'fortune']):
        return 'large'
    
    return None

def extract_job_type(text: str) -> Optional[str]:
    """Extract job type from text"""
    text_lower = text.lower()
    
    if 'full-time' in text_lower or 'full time' in text_lower:
        return 'full-time'
    elif 'part-time' in text_lower or 'part time' in text_lower:
        return 'part-time'
    elif 'contract' in text_lower or 'contractor' in text_lower:
        return 'contract'
    elif 'intern' in text_lower or 'internship' in text_lower:
        return 'internship'
    elif 'freelance' in text_lower:
        return 'freelance'
    elif 'temporary' in text_lower or 'temp' in text_lower:
        return 'temporary'
    
    return None

def extract_experience_level(text: str) -> Optional[str]:
    """Extract experience level from text"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['entry', 'junior', 'entry-level', 'graduate', '0-2 years']):
        return 'entry-level'
    elif any(word in text_lower for word in ['mid', 'mid-level', 'intermediate', '2-5 years', '3-7 years']):
        return 'mid-level'
    elif any(word in text_lower for word in ['senior', 'sr.', 'lead', '5+ years', '7+ years']):
        return 'senior'
    elif any(word in text_lower for word in ['principal', 'staff', 'architect', '10+ years']):
        return 'principal'
    elif any(word in text_lower for word in ['executive', 'director', 'vp', 'chief', 'head']):
        return 'executive'
    
    return None

def clean_html(text: str) -> str:
    """Remove HTML tags from text"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:,.2f}"
    return f"{amount:,.2f} {currency}"

def calculate_days_ago(date: datetime) -> int:
    """Calculate days ago from given date"""
    return (datetime.now() - date).days

def normalize_job_title(title: str) -> str:
    """Normalize job title for better matching"""
    # Common variations to normalize
    normalizations = {
        'sr.': 'senior',
        'jr.': 'junior',
        'dev': 'developer',
        'eng': 'engineer',
        'mgr': 'manager',
        'admin': 'administrator',
        'spec': 'specialist',
        'coord': 'coordinator'
    }
    
    title_lower = title.lower()
    for old, new in normalizations.items():
        title_lower = title_lower.replace(old, new)
    
    return title_lower.title()

def extract_skills_from_text(text: str) -> List[str]:
    """Extract technical skills from text using patterns"""
    
    # Common technical skills patterns
    skill_patterns = [
        # Programming languages
        r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin|Scala)\b',
        
        # Web technologies
        r'\b(?:React|Angular|Vue|Node\.js|Express|Django|Flask|Spring|Laravel|Rails)\b',
        
        # Databases
        r'\b(?:MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle|SQL Server|SQLite)\b',
        
        # Cloud platforms
        r'\b(?:AWS|Azure|GCP|Google Cloud|Kubernetes|Docker|Jenkins|GitLab|GitHub)\b',
        
        # Other technologies
        r'\b(?:Git|REST|GraphQL|API|Machine Learning|AI|DevOps|Agile|Scrum|CI/CD)\b'
    ]
    
    skills = set()
    
    for pattern in skill_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            skills.add(match.group())
    
    return list(skills)

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity score"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def validate_job_data(job_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate job data and return validation errors"""
    errors = {
        "required_fields": [],
        "format_errors": [],
        "value_errors": []
    }
    
    # Required fields
    required_fields = ['title', 'company']
    for field in required_fields:
        if not job_data.get(field):
            errors["required_fields"].append(f"{field} is required")
    
    # Format validations
    if job_data.get('job_url') and not job_data['job_url'].startswith(('http://', 'https://')):
        errors["format_errors"].append("Invalid job URL format")
    
    # Value validations
    if job_data.get('salary_min') and job_data.get('salary_max'):
        if job_data['salary_min'] > job_data['salary_max']:
            errors["value_errors"].append("Minimum salary cannot be greater than maximum salary")
    
    return errors