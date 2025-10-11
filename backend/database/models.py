"""
Database models using SQLAlchemy ORM.
Defines the schema for users, jobs, applications, etc.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(50))
    location = Column(String(255))
    linkedin_url = Column(String(500))
    portfolio_url = Column(String(500))
    preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")
    job_matches = relationship("JobMatch", back_populates="user")
    credentials = relationship("Credential", back_populates="user")


class Resume(Base):
    """Resume model."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50))
    parsed_data = Column(JSON)
    skills = Column(JSON)
    experience = Column(JSON)
    education = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="resumes")


class JobListing(Base):
    """Job listing model."""
    __tablename__ = "job_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255))
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    job_type = Column(String(50))
    experience_level = Column(String(50))
    url = Column(String(500), unique=True)
    source = Column(String(100))
    scraped_at = Column(DateTime, default=datetime.utcnow)
    posted_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    applications = relationship("Application", back_populates="job")
    job_matches = relationship("JobMatch", back_populates="job")


class Application(Base):
    """Job application model."""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_listings.id"), nullable=False)
    status = Column(String(50), default="draft")  # draft, applied, in_review, interview, rejected, accepted
    cover_letter = Column(Text)
    custom_responses = Column(JSON)
    applied_at = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tracking_info = Column(JSON)
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("JobListing", back_populates="applications")


class JobMatch(Base):
    """Job match scoring model."""
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_listings.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    reasoning = Column(Text)
    strengths = Column(JSON)
    gaps = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="job_matches")
    job = relationship("JobListing", back_populates="job_matches")


class Credential(Base):
    """Encrypted credentials model."""
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(100), nullable=False)  # linkedin, indeed, etc.
    encrypted_data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="credentials")
