#!/usr/bin/env python3
"""
Database setup script for AutoAgentHire
Creates all necessary tables and indexes
"""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, Index
from app.core.config import settings
from app.core.database import Base
from app.models.user import User
from app.models.job import Job
from app.models.application import Application

def create_database_and_tables():
    """Create database and all tables"""
    try:
        print("Creating database connection...")
        engine = create_engine(settings.database_url)
        
        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        
        # Create additional indexes for better performance
        print("Creating indexes...")
        create_indexes(engine)
        
        print("✅ Database setup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

def create_indexes(engine):
    """Create additional database indexes for performance"""
    try:
        with engine.connect() as conn:
            # User indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)")
            
            # Job indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs(job_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_remote ON jobs(remote_option)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(is_active)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_scraped_at ON jobs(scraped_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_linkedin_id ON jobs(linkedin_job_id)")
            
            # Application indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_job_id ON applications(job_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_date ON applications(application_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_automated ON applications(automated)")
            
            # Composite indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_applications_user_status ON applications(user_id, status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jobs_location_type ON jobs(location, job_type)")
            
            conn.commit()
            
    except Exception as e:
        print(f"Warning: Could not create some indexes: {e}")

def create_sample_data():
    """Create sample data for testing (optional)"""
    from sqlalchemy.orm import sessionmaker
    from app.core.security import get_password_hash
    from datetime import datetime
    
    try:
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Check if sample user already exists
        existing_user = db.query(User).filter(User.email == "demo@autoagenthire.com").first()
        if existing_user:
            print("Sample data already exists, skipping...")
            return
        
        print("Creating sample data...")
        
        # Create sample user
        sample_user = User(
            email="demo@autoagenthire.com",
            hashed_password=get_password_hash("demo123"),
            full_name="Demo User",
            is_active=True,
            is_verified=True
        )
        db.add(sample_user)
        db.commit()
        db.refresh(sample_user)
        
        # Create sample jobs
        sample_jobs = [
            Job(
                title="Senior Python Developer",
                company="TechCorp Inc.",
                location="San Francisco, CA",
                job_type="full-time",
                experience_level="senior",
                description="We are looking for a Senior Python Developer to join our team...",
                requirements="5+ years Python experience, Django, PostgreSQL",
                salary_min=120000,
                salary_max=160000,
                remote_option=True,
                posted_date=datetime.utcnow(),
                is_active=True
            ),
            Job(
                title="Frontend React Developer",
                company="StartupXYZ",
                location="Remote",
                job_type="full-time",
                experience_level="mid-level",
                description="Join our fast-growing startup as a React Developer...",
                requirements="3+ years React experience, TypeScript, Redux",
                salary_min=90000,
                salary_max=120000,
                remote_option=True,
                posted_date=datetime.utcnow(),
                is_active=True
            ),
            Job(
                title="Data Scientist",
                company="DataAnalytics Co.",
                location="New York, NY",
                job_type="full-time",
                experience_level="mid-level",
                description="Seeking a Data Scientist to analyze large datasets...",
                requirements="Python, Machine Learning, SQL, Statistics",
                salary_min=100000,
                salary_max=140000,
                remote_option=False,
                posted_date=datetime.utcnow(),
                is_active=True
            )
        ]
        
        for job in sample_jobs:
            db.add(job)
        
        db.commit()
        print("✅ Sample data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    print("🚀 Starting AutoAgentHire database setup...")
    
    # Create tables
    create_database_and_tables()
    
    # Ask if user wants sample data
    if len(sys.argv) > 1 and sys.argv[1] == "--sample-data":
        create_sample_data()
    
    print("🎉 Database setup complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and update with your settings")
    print("2. Install Python dependencies: pip install -r backend/requirements.txt")
    print("3. Start the backend: cd backend && uvicorn app.main:app --reload")
    print("4. Install frontend dependencies: cd frontend && npm install")
    print("5. Start the frontend: npm start")