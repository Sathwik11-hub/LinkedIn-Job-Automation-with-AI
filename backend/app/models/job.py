from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    job_type = Column(String)  # full-time, part-time, contract, etc.
    experience_level = Column(String)  # entry-level, mid-level, senior, etc.
    salary_min = Column(Float)
    salary_max = Column(Float)
    description = Column(Text)
    requirements = Column(Text)
    linkedin_job_id = Column(String, unique=True)
    job_url = Column(String)
    company_size = Column(String)
    industry = Column(String)
    skills_required = Column(Text)  # JSON string of skills
    remote_option = Column(Boolean, default=False)
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)