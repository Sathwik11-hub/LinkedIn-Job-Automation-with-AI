import pytest
from app.services.ai.resume_parser import ResumeParser

def test_resume_parser_initialization():
    """Test that ResumeParser can be initialized"""
    parser = ResumeParser()
    assert parser is not None

def test_empty_resume_parsing():
    """Test parsing empty resume text"""
    parser = ResumeParser()
    result = parser.parse_resume("")
    
    assert "skills" in result
    assert "experience" in result
    assert "education" in result
    assert "contact_info" in result
    assert "summary" in result
    
    assert isinstance(result["skills"], list)
    assert isinstance(result["experience"], list)
    assert isinstance(result["education"], list)
    assert isinstance(result["contact_info"], dict)

def test_skill_extraction():
    """Test basic skill extraction"""
    parser = ResumeParser()
    sample_text = "I have experience with Python, JavaScript, React, and AWS."
    
    result = parser.parse_resume(sample_text)
    skills = result["skills"]
    
    # Should find at least some of these skills
    expected_skills = ["Python", "JavaScript", "React", "AWS"]
    found_skills = [skill for skill in expected_skills if any(skill.lower() in s.lower() for s in skills)]
    
    assert len(found_skills) > 0