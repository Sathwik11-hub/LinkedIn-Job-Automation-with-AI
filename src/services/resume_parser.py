"""Resume parser service using spaCy and PyMuPDF."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import fitz  # PyMuPDF
import spacy
from spacy.matcher import Matcher

from ..core import LoggerMixin, get_settings
from ..models import ResumeData


class ResumeParser(LoggerMixin):
    """Resume parser using spaCy NLP and PyMuPDF for PDF processing."""
    
    def __init__(self):
        self.settings = get_settings()
        self.nlp = None
        self.matcher = None
        self._load_nlp_model()
        
    def _load_nlp_model(self):
        """Load spaCy NLP model."""
        try:
            # Try to load the model
            self.nlp = spacy.load("en_core_web_sm")
            self.matcher = Matcher(self.nlp.vocab)
            self._setup_patterns()
            self.logger.info("spaCy model loaded successfully")
        except OSError:
            self.logger.warning(
                "spaCy 'en_core_web_sm' model not found. "
                "Install it with: python -m spacy download en_core_web_sm"
            )
            # Use a basic tokenizer if model not available
            self.nlp = spacy.blank("en")
            self.matcher = Matcher(self.nlp.vocab)
    
    def _setup_patterns(self):
        """Setup patterns for entity extraction."""
        # Email pattern
        email_pattern = [{"TEXT": {"REGEX": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}]
        self.matcher.add("EMAIL", [email_pattern])
        
        # Phone pattern
        phone_pattern = [{"TEXT": {"REGEX": r"(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"}}]
        self.matcher.add("PHONE", [phone_pattern])
    
    def parse_pdf(self, file_path: str) -> ResumeData:
        """Parse resume PDF and extract structured data."""
        self.logger.info(f"Parsing resume: {file_path}")
        
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(file_path)
            
            # Parse the text
            resume_data = self._parse_text(text)
            resume_data.file_path = file_path
            
            self.logger.info("Resume parsed successfully")
            return resume_data
            
        except Exception as e:
            self.logger.error(f"Failed to parse resume: {str(e)}")
            raise
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return text.strip()
            
        except Exception as e:
            self.logger.error(f"Failed to extract text from PDF: {str(e)}")
            raise
    
    def _parse_text(self, text: str) -> ResumeData:
        """Parse resume text and extract structured information."""
        doc = self.nlp(text)
        
        # Extract basic information
        name = self._extract_name(text, doc)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        # Extract sections
        skills = self._extract_skills(text, doc)
        experience = self._extract_experience(text)
        education = self._extract_education(text)
        summary = self._extract_summary(text)
        
        return ResumeData(
            file_path="",  # Will be set by caller
            name=name,
            email=email,
            phone=phone,
            skills=skills,
            experience=experience,
            education=education,
            summary=summary
        )
    
    def _extract_name(self, text: str, doc) -> Optional[str]:
        """Extract candidate name from resume."""
        # Try to find name in the first few lines
        lines = text.split('\n')[:5]
        
        for line in lines:
            line = line.strip()
            if len(line) > 0 and len(line.split()) <= 4:
                # Check if it looks like a name (contains only letters and spaces)
                if re.match(r'^[A-Za-z\s]+$', line):
                    return line
        
        # Fallback: use spaCy to find person entities
        if hasattr(doc, 'ents'):
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    return ent.text
        
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from resume."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from resume."""
        # Various phone number patterns
        phone_patterns = [
            r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\+?([0-9]{1,3})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Join the groups to form complete phone number
                if isinstance(matches[0], tuple):
                    return ''.join(matches[0])
                else:
                    return matches[0]
        
        return None
    
    def _extract_skills(self, text: str, doc) -> List[str]:
        """Extract skills from resume."""
        skills = []
        
        # Common technical skills keywords
        skill_keywords = [
            # Programming languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'xml', 'json',
            
            # Frameworks and libraries
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'nodejs', 'express',
            'jquery', 'bootstrap', 'tensorflow', 'pytorch', 'keras', 'pandas', 'numpy', 'scikit-learn',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'terraform',
            'ansible', 'chef', 'puppet', 'nagios', 'prometheus', 'grafana',
            
            # Tools and technologies
            'git', 'svn', 'jira', 'confluence', 'slack', 'linux', 'windows', 'macos', 'bash', 'powershell',
            'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'kanban', 'devops', 'ci/cd',
            
            # Data and Analytics
            'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision', 'data science',
            'data analysis', 'big data', 'hadoop', 'spark', 'tableau', 'powerbi', 'excel'
        ]
        
        # Look for skills section
        skills_section = self._extract_section(text, ['skills', 'technical skills', 'technologies'])
        if skills_section:
            text_to_analyze = skills_section
        else:
            text_to_analyze = text
        
        # Find skills in text (case insensitive)
        text_lower = text_to_analyze.lower()
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                # Verify it's a whole word match
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                    skills.append(skill.title())
        
        # Remove duplicates and sort
        skills = sorted(list(set(skills)))
        
        return skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience from resume."""
        experience = []
        
        # Look for experience section
        exp_section = self._extract_section(text, [
            'experience', 'work experience', 'professional experience', 
            'employment', 'career history', 'work history'
        ])
        
        if not exp_section:
            return experience
        
        # Split by potential job entries (look for date patterns)
        date_pattern = r'\b(20\d{2}|19\d{2})\b'
        lines = exp_section.split('\n')
        
        current_job = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line contains dates (likely job period)
            if re.search(date_pattern, line):
                if current_job:
                    experience.append(current_job)
                current_job = {'period': line}
            elif not current_job.get('title') and len(line.split()) <= 6:
                # Likely job title
                current_job['title'] = line
            elif not current_job.get('company') and len(line.split()) <= 4:
                # Likely company name
                current_job['company'] = line
            else:
                # Description
                if 'description' not in current_job:
                    current_job['description'] = line
                else:
                    current_job['description'] += ' ' + line
        
        # Add the last job
        if current_job:
            experience.append(current_job)
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education from resume."""
        education = []
        
        # Look for education section
        edu_section = self._extract_section(text, [
            'education', 'academic background', 'qualifications', 'degrees'
        ])
        
        if not edu_section:
            return education
        
        # Common degree patterns
        degree_patterns = [
            r'\b(bachelor|master|phd|doctorate|associate|diploma|certificate)\b',
            r'\b(b\.?[sa]\.?|m\.?[sa]\.?|ph\.?d\.?|m\.?d\.?|j\.?d\.?)\b',
            r'\b(undergraduate|graduate|postgraduate)\b'
        ]
        
        lines = edu_section.split('\n')
        current_edu = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line contains degree information
            line_lower = line.lower()
            for pattern in degree_patterns:
                if re.search(pattern, line_lower):
                    if current_edu:
                        education.append(current_edu)
                    current_edu = {'degree': line}
                    break
            else:
                # Check for university/institution
                if 'university' in line_lower or 'college' in line_lower or 'institute' in line_lower:
                    current_edu['institution'] = line
                elif re.search(r'\b(20\d{2}|19\d{2})\b', line):
                    current_edu['year'] = line
        
        # Add the last education entry
        if current_edu:
            education.append(current_edu)
        
        return education
    
    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary from resume."""
        # Look for summary section
        summary_keywords = [
            'summary', 'objective', 'profile', 'about', 'overview', 
            'professional summary', 'career objective'
        ]
        
        summary_section = self._extract_section(text, summary_keywords)
        if summary_section:
            # Clean up and return first paragraph
            lines = [line.strip() for line in summary_section.split('\n') if line.strip()]
            if lines:
                return ' '.join(lines[:3])  # Take first 3 lines
        
        # Fallback: take first meaningful paragraph
        paragraphs = text.split('\n\n')
        for para in paragraphs[:3]:
            para = para.strip()
            if len(para) > 50 and not re.search(r'@|\+\d|\d{4}', para):
                return para
        
        return None
    
    def _extract_section(self, text: str, keywords: List[str]) -> Optional[str]:
        """Extract specific section from resume text."""
        lines = text.split('\n')
        section_start = -1
        
        # Find section start
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            for keyword in keywords:
                if keyword.lower() in line_lower and len(line_lower) < 50:
                    section_start = i + 1
                    break
            if section_start != -1:
                break
        
        if section_start == -1:
            return None
        
        # Find section end (next section header or end of document)
        section_end = len(lines)
        for i in range(section_start, len(lines)):
            line = lines[i].strip()
            if (len(line) > 0 and len(line) < 50 and 
                any(keyword in line.lower() for keyword in [
                    'experience', 'education', 'skills', 'projects', 
                    'certifications', 'achievements', 'awards'
                ]) and
                not any(keyword.lower() in line.lower() for keyword in keywords)):
                section_end = i
                break
        
        section_text = '\n'.join(lines[section_start:section_end])
        return section_text.strip() if section_text.strip() else None