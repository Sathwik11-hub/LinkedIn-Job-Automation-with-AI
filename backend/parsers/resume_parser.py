"""
Resume parser - Extracts information from resumes.
Supports PDF, DOCX, and TXT formats.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not installed - PDF parsing disabled")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    logger.warning("python-docx not installed - DOCX parsing disabled")


class ResumeParser:
    """
    Parser for extracting information from resumes.
    """
    
    def __init__(self):
        """Initialize the resume parser."""
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a resume file and extract structured information.
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            Dictionary with extracted information
        """
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        file_ext = file_path_obj.suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        
        # Extract text based on file type
        if file_ext == '.pdf':
            text = self._extract_from_pdf(file_path)
        elif file_ext == '.docx':
            text = self._extract_from_docx(file_path)
        else:
            text = self._extract_from_txt(file_path)
        
        # Parse the extracted text
        parsed_data = self._parse_text(text)
        
        return parsed_data
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        if not PDF_AVAILABLE:
            return "PDF parsing not available - PyPDF2 not installed"
        
        try:
            text = []
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            return ""
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        if not DOCX_AVAILABLE:
            return "DOCX parsing not available - python-docx not installed"
        
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Error extracting DOCX: {e}")
            return ""
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _parse_text(self, text: str) -> Dict[str, Any]:
        """
        Parse extracted text to structured data.
        
        Args:
            text: Raw text from resume
            
        Returns:
            Structured resume data
        """
        # TODO: Implement text parsing logic
        # 1. Extract contact info (name, email, phone)
        # 2. Extract work experience
        # 3. Extract education
        # 4. Extract skills
        # 5. Extract certifications
        
        return {
            "contact": {},
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "raw_text": text
        }


# Helper function for backward compatibility
def extract_resume_text(file_path: str) -> str:
    """
    Extract raw text from a resume file.
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        Extracted text from the resume
    """
    parser = ResumeParser()
    result = parser.parse(file_path)
    return result.get("raw_text", "")
