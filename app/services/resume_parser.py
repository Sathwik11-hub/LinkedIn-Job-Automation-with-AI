"""
Resume parsing service using NLP
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import spacy
from spacy.matcher import Matcher
import fitz  # PyMuPDF
from docx import Document

from app.models.job_schema import Resume
from app.utils.logger import setup_logger, log_performance
from app.config import settings

logger = setup_logger(__name__)


class ResumeParser:
    """
    NLP-based resume parser
    """
    
    def __init__(self):
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model: en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found, using basic text processing")
            self.nlp = None
        
        # Initialize matcher for skills extraction
        self.matcher = Matcher(self.nlp.vocab) if self.nlp else None
        self._setup_skill_patterns()
        
        # Common skills database (simplified)
        self.skill_database = self._load_skill_database()
    
    def _setup_skill_patterns(self):
        """Setup spaCy patterns for skill extraction"""
        if not self.matcher:
            return
        
        # Programming languages
        programming_patterns = [
            [{"LOWER": {"IN": ["python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "swift"]}}],
            [{"LOWER": "react"}, {"LOWER": {"IN": ["js", "native"]}, "OP": "?"}],
            [{"LOWER": "node"}, {"LOWER": {"IN": ["js", ".js"]}, "OP": "?"}],
            [{"LOWER": "machine"}, {"LOWER": "learning"}],
            [{"LOWER": "data"}, {"LOWER": {"IN": ["science", "analysis", "analytics"]}}],
        ]
        
        for pattern in programming_patterns:
            self.matcher.add("PROGRAMMING_SKILL", [pattern])
        
        # Frameworks and tools
        tool_patterns = [
            [{"LOWER": {"IN": ["docker", "kubernetes", "aws", "azure", "gcp", "tensorflow", "pytorch"]}}],
            [{"LOWER": "sql"}, {"LOWER": {"IN": ["server", "database"]}, "OP": "?"}],
            [{"LOWER": {"IN": ["git", "github", "gitlab", "bitbucket"]}}],
        ]
        
        for pattern in tool_patterns:
            self.matcher.add("TOOL_SKILL", [pattern])
    
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skills database"""
        return {
            "programming_languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Swift",
                "Kotlin", "Scala", "R", "MATLAB", "PHP", "Ruby", "Perl", "Haskell", "Clojure"
            ],
            "web_technologies": [
                "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask",
                "Spring Boot", "ASP.NET", "Laravel", "Ruby on Rails", "HTML", "CSS", "SASS", "LESS"
            ],
            "databases": [
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite",
                "Oracle", "SQL Server", "DynamoDB", "Cassandra", "Neo4j"
            ],
            "cloud_platforms": [
                "AWS", "Azure", "Google Cloud", "DigitalOcean", "Heroku", "Vercel", "Netlify"
            ],
            "devops_tools": [
                "Docker", "Kubernetes", "Jenkins", "Git", "GitHub", "GitLab", "Ansible",
                "Terraform", "Chef", "Puppet", "Vagrant", "CircleCI", "Travis CI"
            ],
            "data_science": [
                "Machine Learning", "Deep Learning", "Data Science", "Data Analysis",
                "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Matplotlib",
                "Seaborn", "Jupyter", "Apache Spark", "Hadoop", "Tableau", "Power BI"
            ],
            "soft_skills": [
                "Leadership", "Communication", "Problem Solving", "Team Management",
                "Project Management", "Agile", "Scrum", "Critical Thinking", "Creativity",
                "Adaptability", "Time Management", "Collaboration"
            ]
        }
    
    @log_performance
    def parse_resume(self, file_path: str) -> Resume:
        """
        Parse resume from file
        
        Args:
            file_path: Path to resume file (PDF, DOCX, or TXT)
            
        Returns:
            Resume object with extracted information
        """
        try:
            # Extract text from file
            text = self._extract_text_from_file(file_path)
            
            if not text:
                raise ValueError("Could not extract text from resume file")
            
            # Parse resume components
            resume_data = self._parse_resume_text(text)
            
            # Create Resume object
            resume = Resume(**resume_data)
            
            logger.info(f"Successfully parsed resume: {resume.name}")
            return resume
            
        except Exception as e:
            logger.error(f"Error parsing resume {file_path}: {e}")
            raise
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        try:
            if file_path.suffix.lower() == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                return self._extract_from_docx(file_path)
            elif file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page in doc:
                text += page.get_text()
            
            doc.close()
            return text
            
        except Exception as e:
            logger.error(f"Error extracting from PDF: {e}")
            return ""
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting from DOCX: {e}")
            return ""
    
    @log_performance
    def _parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured information"""
        
        # Clean text
        text = self._clean_text(text)
        
        # Extract basic information
        name = self._extract_name(text)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        location = self._extract_location(text)
        
        # Extract sections
        summary = self._extract_summary(text)
        skills = self._extract_skills(text)
        experience = self._extract_experience(text)
        education = self._extract_education(text)
        certifications = self._extract_certifications(text)
        
        # Calculate derived information
        years_experience = self._calculate_experience_years(experience)
        key_achievements = self._extract_achievements(text)
        technical_skills, soft_skills = self._categorize_skills(skills)
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "summary": summary,
            "skills": skills,
            "experience": experience,
            "education": education,
            "certifications": certifications,
            "years_experience": years_experience,
            "key_achievements": key_achievements,
            "technical_skills": technical_skills,
            "soft_skills": soft_skills
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep line breaks for section detection
        text = re.sub(r'[^\w\s\n\.\@\-\(\)\+]', ' ', text)
        return text.strip()
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name (simplified)"""
        lines = text.split('\n')
        
        # Usually name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            # Skip email lines, phone lines, etc.
            if '@' in line or re.search(r'\d{10}', line) or len(line.split()) > 4:
                continue
            
            # Check if line looks like a name
            words = line.split()
            if 2 <= len(words) <= 4 and all(word.isalpha() for word in words):
                return ' '.join(words).title()
        
        return "Unknown Candidate"
    
    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else "email@example.com"
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\b\d{10}\b'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return str(matches[0]) if isinstance(matches[0], str) else ''.join(matches[0])
        
        return None
    
    def _extract_location(self, text: str) -> str:
        """Extract location (simplified)"""
        # Look for common location patterns
        location_patterns = [
            r'([A-Z][a-z]+,\s*[A-Z]{2})',  # City, State
            r'([A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2})',  # City Name, State
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return "Location not specified"
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        # Look for summary section
        summary_keywords = ['summary', 'objective', 'profile', 'about']
        
        lines = text.split('\n')
        summary_start = -1
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                summary_start = i
                break
        
        if summary_start >= 0:
            # Extract next few lines as summary
            summary_lines = []
            for i in range(summary_start + 1, min(summary_start + 5, len(lines))):
                line = lines[i].strip()
                if line and not any(keyword in line.lower() for keyword in ['experience', 'education', 'skills']):
                    summary_lines.append(line)
                else:
                    break
            
            return ' '.join(summary_lines)
        
        # Fallback: use first paragraph as summary
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs[1:3]:  # Skip first paragraph (usually name/contact)
            if len(paragraph.split()) > 10:
                return paragraph.strip()
        
        return "Professional summary not available"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        skills = set()
        
        # Use spaCy matcher if available
        if self.nlp and self.matcher:
            doc = self.nlp(text.lower())
            matches = self.matcher(doc)
            
            for match_id, start, end in matches:
                skill = doc[start:end].text
                skills.add(skill.title())
        
        # Also check against skill database
        text_lower = text.lower()
        for category, skill_list in self.skill_database.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.add(skill)
        
        return list(skills)
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience (simplified)"""
        # This is a basic implementation
        # A full implementation would use more sophisticated NLP
        
        experience = []
        
        # Look for experience section
        lines = text.split('\n')
        in_experience_section = False
        
        for line in lines:
            line = line.strip()
            
            if 'experience' in line.lower() and len(line.split()) <= 3:
                in_experience_section = True
                continue
            
            if in_experience_section:
                # Stop if we hit another section
                if any(keyword in line.lower() for keyword in ['education', 'skills', 'projects']):
                    break
                
                # Look for job title patterns
                if len(line.split()) >= 2 and not line.startswith('-'):
                    experience.append({
                        "title": line,
                        "company": "Company Name",
                        "duration": "2020-2023",
                        "description": "Job responsibilities and achievements"
                    })
        
        return experience[:5]  # Limit to top 5 experiences
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information (simplified)"""
        education = []
        
        # Look for degree keywords
        degree_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in degree_keywords):
                education.append({
                    "degree": line.strip(),
                    "institution": "University Name",
                    "year": "2020",
                    "gpa": None
                })
        
        return education[:3]  # Limit to top 3 education entries
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        # Common certification keywords
        cert_keywords = [
            'certified', 'certification', 'aws', 'azure', 'google cloud',
            'pmp', 'cissp', 'comptia', 'cisco', 'microsoft'
        ]
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications[:5]  # Limit to top 5 certifications
    
    def _calculate_experience_years(self, experience: List[Dict[str, Any]]) -> Optional[int]:
        """Calculate total years of experience"""
        # Simplified calculation
        return min(len(experience) * 2, 20) if experience else 0
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extract key achievements"""
        achievements = []
        
        # Look for achievement indicators
        achievement_patterns = [
            r'(?i)(increased|improved|reduced|led|managed|developed|created|implemented|achieved).*?(\d+%|\$\d+|[0-9,]+\s*users)',
            r'(?i)(award|recognition|promoted|selected)'
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text)
            achievements.extend([match[0] if isinstance(match, tuple) else match for match in matches])
        
        return achievements[:5]  # Limit to top 5 achievements
    
    def _categorize_skills(self, skills: List[str]) -> tuple[List[str], List[str]]:
        """Categorize skills into technical and soft skills"""
        technical_skills = []
        soft_skills = []
        
        technical_categories = ['programming_languages', 'web_technologies', 'databases', 'cloud_platforms', 'devops_tools', 'data_science']
        
        for skill in skills:
            is_technical = False
            for category in technical_categories:
                if skill in self.skill_database.get(category, []):
                    technical_skills.append(skill)
                    is_technical = True
                    break
            
            if not is_technical and skill in self.skill_database.get('soft_skills', []):
                soft_skills.append(skill)
        
        return technical_skills, soft_skills