from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    APPLIED = "applied" 
    VIEWED = "viewed"
    REJECTED = "rejected"
    INTERVIEW_REQUESTED = "interview_requested"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"
    DECLINED = "declined"

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    cover_letter = Column(Text)
    custom_resume_path = Column(String)
    application_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = Column(Text)
    interview_date = Column(DateTime)
    response_received = Column(Boolean, default=False)
    automated = Column(Boolean, default=True)
    success_score = Column(Integer)  # AI-generated compatibility score
    
    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")