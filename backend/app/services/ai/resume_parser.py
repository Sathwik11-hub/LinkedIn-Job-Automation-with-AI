import PyPDF2
import pdfplumber
import spacy
import re
from typing import Dict, List, Optional
from pathlib import Path

class ResumeParser:
    def __init__(self):
        # Try to load spaCy model, use a simple fallback if not available
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found. Using basic parsing.")
            self.nlp = None
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        text = ""
        
        try:
            # Try pdfplumber first (better for complex layouts)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2")
            
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PyPDF2 also failed: {e}")
                return ""
        
        return text.strip()
    
    def parse_resume(self, resume_text: str) -> Dict:
        """Parse resume text and extract structured information"""
        if not resume_text:
            return self._empty_resume_data()
        
        resume_data = {
            "skills": self._extract_skills(resume_text),
            "experience": self._extract_experience(resume_text),
            "education": self._extract_education(resume_text),
            "contact_info": self._extract_contact_info(resume_text),
            "summary": self._extract_summary(resume_text)
        }
        
        return resume_data
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        
        # Common skill keywords
        skill_patterns = [
            r'Python', r'Java', r'JavaScript', r'TypeScript', r'C\+\+', r'C#',
            r'React', r'Angular', r'Vue\.js', r'Node\.js', r'Django', r'Flask',
            r'SQL', r'PostgreSQL', r'MySQL', r'MongoDB', r'Redis',
            r'AWS', r'Azure', r'GCP', r'Docker', r'Kubernetes',
            r'Git', r'Jenkins', r'CI/CD', r'DevOps',
            r'Machine Learning', r'AI', r'Data Science', r'TensorFlow', r'PyTorch',
            r'HTML', r'CSS', r'REST API', r'GraphQL',
            r'Agile', r'Scrum', r'Project Management'
        ]
        
        text_upper = text.upper()
        
        for pattern in skill_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                skills.append(pattern.replace(r'\.', '.').replace(r'\+', '+'))
        
        # Look for skills sections
        skills_section = self._find_section(text, ['skills', 'technical skills', 'technologies'])
        if skills_section:
            # Extract comma-separated skills
            skill_lines = re.findall(r'[A-Za-z][A-Za-z0-9\+\.\#\s-]+', skills_section)
            for line in skill_lines:
                if len(line.strip()) > 2 and len(line.strip()) < 30:
                    skills.append(line.strip())
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from resume"""
        experience = []
        
        # Look for experience section
        exp_section = self._find_section(text, ['experience', 'work experience', 'employment', 'professional experience'])
        
        if exp_section:
            # Simple pattern to find job titles and companies
            job_patterns = re.findall(
                r'([A-Z][A-Za-z\s]+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator|Assistant|Director))\s*(?:at|@)?\s*([A-Z][A-Za-z\s&,\.]+?)(?:\n|\d{4})',
                exp_section,
                re.MULTILINE
            )
            
            for job_title, company in job_patterns:
                experience.append({
                    "title": job_title.strip(),
                    "company": company.strip(),
                    "duration": "Not specified",
                    "description": "Not extracted"
                })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        edu_section = self._find_section(text, ['education', 'academic background', 'qualification'])
        
        if edu_section:
            # Look for degree patterns
            degree_patterns = re.findall(
                r'(Bachelor|Master|PhD|B\.S\.|M\.S\.|B\.A\.|M\.A\.|B\.Tech|M\.Tech)[A-Za-z\s,]*(?:in\s+)?([A-Za-z\s]+?)(?:from\s+)?([A-Z][A-Za-z\s&,\.]+?)(?:\n|\d{4})',
                edu_section,
                re.IGNORECASE
            )
            
            for degree_type, field, institution in degree_patterns:
                education.append({
                    "degree": f"{degree_type} in {field}".strip(),
                    "institution": institution.strip(),
                    "year": "Not specified"
                })
        
        return education
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            contact['phone'] = phone_match.group()
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        return contact
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary or objective"""
        summary_section = self._find_section(text, ['summary', 'objective', 'profile', 'about'])
        
        if summary_section:
            # Take first few sentences
            sentences = re.split(r'[.!?]+', summary_section)
            if sentences:
                return '. '.join(sentences[:3]).strip() + '.'
        
        return "No summary found"
    
    def _find_section(self, text: str, section_names: List[str]) -> Optional[str]:
        """Find a specific section in the resume text"""
        for section_name in section_names:
            pattern = rf'{section_name}:?\s*\n(.*?)(?:\n\n|\n[A-Z][A-Za-z\s]+:|\Z)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return None
    
    def _empty_resume_data(self) -> Dict:
        """Return empty resume data structure"""
        return {
            "skills": [],
            "experience": [],
            "education": [],
            "contact_info": {},
            "summary": "No resume data available"
        }