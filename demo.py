#!/usr/bin/env python3
"""
Sample usage script for AutoAgentHire
Demonstrates how to use the API programmatically
"""

import asyncio
import aiohttp
import json
from pathlib import Path

class AutoAgentHireClient:
    """Simple client for AutoAgentHire API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_jobs(self, keywords: str, location: str = "United States", limit: int = 10):
        """Search for jobs"""
        async with self.session.post(
            f"{self.base_url}/api/v1/jobs/search",
            json={
                "keywords": keywords,
                "location": location,
                "limit": limit
            }
        ) as response:
            return await response.json()
    
    async def match_jobs(self, keywords: str, resume_path: str, location: str = "United States"):
        """Find matching jobs for a resume"""
        async with self.session.post(
            f"{self.base_url}/api/v1/jobs/match",
            json={
                "keywords": keywords,
                "location": location,
                "resume_path": resume_path,
                "include_match_score": True,
                "limit": 20
            }
        ) as response:
            return await response.json()
    
    async def apply_to_job(self, job_id: str, resume_path: str):
        """Apply to a specific job"""
        async with self.session.post(
            f"{self.base_url}/api/v1/jobs/apply",
            json={
                "job_id": job_id,
                "resume_path": resume_path,
                "cover_letter_template": "standard"
            }
        ) as response:
            return await response.json()
    
    async def get_application_status(self):
        """Get current application status"""
        async with self.session.get(
            f"{self.base_url}/api/v1/jobs/applications/status"
        ) as response:
            return await response.json()

async def demonstrate_job_search():
    """Demonstrate job search functionality"""
    print("🔍 Demonstrating Job Search...")
    
    async with AutoAgentHireClient() as client:
        try:
            # Search for software engineer jobs
            jobs = await client.search_jobs(
                keywords="software engineer python",
                location="San Francisco, CA",
                limit=5
            )
            
            print(f"Found {len(jobs.get('jobs', []))} jobs")
            
            for job in jobs.get('jobs', [])[:3]:
                print(f"  - {job['title']} at {job['company']} ({job['location']})")
        
        except Exception as e:
            print(f"❌ Error: {e}")

async def demonstrate_ai_matching():
    """Demonstrate AI-powered job matching"""
    print("\n🧠 Demonstrating AI Job Matching...")
    
    # Create a sample resume file path (would be real in actual usage)
    sample_resume = "/path/to/your/resume.pdf"
    
    async with AutoAgentHireClient() as client:
        try:
            # Find matching jobs
            matches = await client.match_jobs(
                keywords="data scientist machine learning",
                resume_path=sample_resume,
                location="New York, NY"
            )
            
            print(f"Found {len(matches)} matching jobs")
            
            # Show top matches
            for job in matches[:3]:
                score = job.get('match_score', 0)
                print(f"  - {job['title']} at {job['company']} (Match: {score:.1%})")
                
                if job.get('match_reasons'):
                    print(f"    Reasons: {', '.join(job['match_reasons'][:2])}")
        
        except Exception as e:
            print(f"❌ Error: {e}")

async def demonstrate_auto_apply():
    """Demonstrate automated job application"""
    print("\n🤖 Demonstrating Automated Application...")
    
    sample_resume = "/path/to/your/resume.pdf"
    sample_job_id = "1234567890"  # Would be real LinkedIn job ID
    
    async with AutoAgentHireClient() as client:
        try:
            # Apply to a job
            result = await client.apply_to_job(
                job_id=sample_job_id,
                resume_path=sample_resume
            )
            
            if result.get('success'):
                print(f"✅ Application submitted successfully!")
                print(f"   Application ID: {result.get('application_id')}")
            else:
                print(f"❌ Application failed: {result.get('message')}")
        
        except Exception as e:
            print(f"❌ Error: {e}")

async def demonstrate_status_tracking():
    """Demonstrate application status tracking"""
    print("\n📊 Demonstrating Status Tracking...")
    
    async with AutoAgentHireClient() as client:
        try:
            status = await client.get_application_status()
            
            print(f"Total Applications: {status.get('total_applications', 0)}")
            print(f"Successful: {status.get('successful_applications', 0)}")
            print(f"Success Rate: {status.get('success_rate', 0):.1f}%")
            print(f"Daily Count: {status.get('daily_count', 0)}/{status.get('daily_limit', 0)}")
        
        except Exception as e:
            print(f"❌ Error: {e}")

def create_sample_config():
    """Create a sample configuration file"""
    print("\n📝 Creating sample configuration...")
    
    sample_config = {
        "job_search": {
            "keywords": ["software engineer", "python developer", "backend engineer"],
            "locations": ["San Francisco, CA", "New York, NY", "Seattle, WA"],
            "job_types": ["full_time"],
            "experience_levels": ["mid_senior"]
        },
        "application_settings": {
            "max_applications_per_day": 10,
            "minimum_match_score": 0.6,
            "auto_apply_enabled": False,
            "cover_letter_template": "standard"
        },
        "resume_paths": {
            "default": "/path/to/your/main_resume.pdf",
            "technical": "/path/to/your/technical_resume.pdf",
            "management": "/path/to/your/management_resume.pdf"
        }
    }
    
    config_file = Path("sample_config.json")
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"✅ Sample configuration saved to {config_file}")
    print("Edit this file with your actual job search criteria and resume paths")

async def main():
    """Main demonstration function"""
    print("🚀 AutoAgentHire - Usage Demonstration")
    print("=" * 50)
    print("Note: This script demonstrates API usage.")
    print("Make sure AutoAgentHire is running at http://localhost:8000")
    print("=" * 50)
    
    # Create sample configuration
    create_sample_config()
    
    # Note: These demonstrations will only work if the server is running
    # and properly configured with LinkedIn credentials
    
    try:
        # Test if server is running
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    print("✅ AutoAgentHire server is running")
                    
                    # Run demonstrations
                    await demonstrate_job_search()
                    await demonstrate_ai_matching()
                    await demonstrate_auto_apply()
                    await demonstrate_status_tracking()
                else:
                    print("❌ Server returned error status")
    
    except aiohttp.ClientError:
        print("❌ AutoAgentHire server is not running")
        print("Start the server with: ./run.sh")
        print("\nDemonstration skipped - server not available")
    
    print("\n" + "=" * 50)
    print("📚 For more examples, check the API documentation at:")
    print("   http://localhost:8000/docs")
    print("\n💡 Tips for getting started:")
    print("1. Configure your LinkedIn credentials in .env")
    print("2. Add your OpenAI API key for AI features")
    print("3. Start with job search to test basic functionality")
    print("4. Use AI matching to find best opportunities")
    print("5. Enable auto-apply for qualified positions")

if __name__ == "__main__":
    asyncio.run(main())