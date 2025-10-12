"""
AutoAgentHire - Clean Auto Apply Agent
Simple, working version with proper error handling.
"""
import os
import asyncio
from typing import Dict, List, Optional
from pathlib import Path

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

from playwright.async_api import async_playwright, Page, Browser
from dotenv import load_dotenv
from backend.utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger(__name__)


class AutoApplyAgent:
    """Clean Auto Apply Agent with proper error handling."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.linkedin_email: Optional[str] = os.getenv("LINKEDIN_EMAIL")
        self.linkedin_password: Optional[str] = os.getenv("LINKEDIN_PASSWORD")
        
        # Initialize Gemini AI if available
        self.gemini_model = None
        if GENAI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
            try:
                # No need to call genai.configure; just ensure the API key is set in the environment
                try:
                    self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
                    logger.info("✅ Gemini AI initialized")
                except AttributeError:
                    logger.warning("⚠️ GenerativeModel not found in google.generativeai")
                    self.gemini_model = None
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Gemini AI: {e}")
    
    async def initialize_browser(self, headless: bool = False) -> bool:
        """Initialize browser with anti-detection features."""
        try:
            playwright = await async_playwright().start()
            
            # Enhanced browser args for stealth
            browser_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            ]
            
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=browser_args
            )
            
            # Create context with realistic settings
            context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                viewport={'width': 1366, 'height': 768}
            )
            
            self.page = await context.new_page()
            logger.info("🤖 Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize browser: {str(e)}")
            return False
    
    async def login_to_linkedin(self) -> bool:
        """Login to LinkedIn."""
        if not self.page:
            logger.error("❌ Browser not initialized")
            return False
        
        if not self.linkedin_email or not self.linkedin_password:
            logger.error("❌ LinkedIn credentials not configured")
            return False
        
        try:
            logger.info("🔐 Logging into LinkedIn...")
            
            # Navigate to login page
            await self.page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            await self.page.wait_for_timeout(2000)
            
            # Check if already logged in
            current_url = self.page.url
            if "feed" in current_url or "in/" in current_url:
                logger.info("✅ Already logged into LinkedIn")
                return True
            
            # Fill credentials
            await self.page.fill('input[name="session_key"]', self.linkedin_email)
            await self.page.wait_for_timeout(500)
            await self.page.fill('input[name="session_password"]', self.linkedin_password)
            await self.page.wait_for_timeout(500)
            
            # Submit login
            await self.page.click('button[type="submit"]')
            await self.page.wait_for_timeout(5000)
            
            # Check login success
            current_url = self.page.url
            if any(indicator in current_url for indicator in ["feed", "in/", "home"]):
                logger.info("✅ LinkedIn login successful")
                return True
            elif "challenge" in current_url or "checkpoint" in current_url:
                logger.warning("⚠️ LinkedIn verification required")
                return False
            else:
                logger.error(f"❌ LinkedIn login failed - URL: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"❌ LinkedIn login error: {str(e)}")
            return False
    
    async def search_jobs(self, keyword: str, location: str = "") -> List[Dict]:
        """Search for jobs on LinkedIn."""
        if not self.page:
            logger.error("❌ Browser not initialized")
            return []
        
        try:
            logger.info(f"🔍 Searching jobs: {keyword} in {location}")
            
            # Construct search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            if location:
                search_url += f"&location={location.replace(' ', '%20')}"
            search_url += "&f_AL=true"  # Easy Apply only
            
            await self.page.goto(search_url, wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Extract job listings
            jobs = []
            try:
                job_elements = await self.page.query_selector_all('.jobs-search-results__list-item')
                
                for i, job_element in enumerate(job_elements[:10]):  # Limit to 10 jobs
                    try:
                        # Extract basic job info
                        title = "Unknown Title"
                        company = "Unknown Company"
                        job_location = "Unknown Location"
                        job_url = ""
                        
                        # Try to extract title
                        title_element = await job_element.query_selector('.base-search-card__title a')
                        if title_element:
                            title = await title_element.inner_text()
                            job_url = await title_element.get_attribute('href') or ""
                            if job_url and not job_url.startswith('http'):
                                job_url = f"https://www.linkedin.com{job_url}"
                        
                        # Try to extract company
                        company_element = await job_element.query_selector('.base-search-card__subtitle')
                        if company_element:
                            company = await company_element.inner_text()
                        
                        # Try to extract location
                        location_element = await job_element.query_selector('.job-search-card__location')
                        if location_element:
                            job_location = await location_element.inner_text()
                        
                        jobs.append({
                            "title": title.strip(),
                            "company": company.strip(),
                            "location": job_location.strip(),
                            "url": job_url,
                            "index": i
                        })
                        
                    except Exception as e:
                        logger.warning(f"Error extracting job {i}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.error(f"Error finding job elements: {str(e)}")
            
            logger.info(f"📊 Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Job search error: {str(e)}")
            return []
    
    async def analyze_job_compatibility(self, job: Dict, resume_text: str) -> Dict:
        """Analyze job compatibility using AI."""
        if not self.gemini_model:
            # Fallback analysis
            return {
                "score": 5,
                "recommendation": "Limited analysis available",
                "strengths": ["General match"],
                "reasoning": "AI analysis not available"
            }
        
        try:
            prompt = f"""
            Analyze this job for compatibility:
            
            Job: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}
            Location: {job.get('location', 'N/A')}
            
            Resume Summary: {resume_text[:800]}
            
            Rate compatibility 1-10 and provide brief reasoning.
            Format: Score: X | Reason: brief explanation
            """
            
            response = self.gemini_model.generate_content(prompt)
            ai_text = response.text.lower()
            
            # Parse response
            score = 5  # default
            try:
                if "score:" in ai_text:
                    score_part = ai_text.split("score:")[1].split("|")[0].strip()
                    score = int(score_part.split()[0])
            except:
                pass
            
            reason_start = ai_text.find("reason:") + 7 if "reason:" in ai_text else 0
            reasoning = ai_text[reason_start:reason_start+200].strip() if reason_start > 6 else "AI analysis completed"
            
            return {
                "score": min(max(score, 1), 10),  # Ensure 1-10 range
                "recommendation": "Apply" if score >= 7 else "Skip",
                "strengths": ["AI analyzed"],
                "reasoning": reasoning[:100]
            }
            
        except Exception as e:
            logger.error(f"AI analysis error: {str(e)}")
            return {
                "score": 5,
                "recommendation": "Analysis failed",
                "strengths": [],
                "reasoning": f"Error: {str(e)}"
            }
    
    async def close_browser(self):
        """Close browser and cleanup."""
        if self.browser:
            await self.browser.close()
            logger.info("🧹 Browser closed")


async def run_autoagent(keyword: str, location: str, resume_path: str, max_jobs: int = 10, similarity_threshold: float = 0.5) -> Dict:
    """
    Main function to run AutoAgent automation.
    This is a simplified version that focuses on core functionality.
    """
    # Validate inputs
    if not os.path.exists(resume_path):
        return {"error": f"Resume file not found: {resume_path}"}
    
    # Initialize results
    results = {
        "total_jobs_found": 0,
        "jobs_analyzed": 0,
        "applications_attempted": 0,
        "applications_successful": 0,
        "jobs": [],
        "summary": "",
        "errors": []
    }
    
    agent = AutoApplyAgent()
    
    try:
        # Extract resume text (simplified)
        resume_text = f"Resume content for {keyword} position"  # Placeholder
        
        # Initialize browser
        if not await agent.initialize_browser(headless=False):
            return {"error": "Failed to initialize browser"}
        
        # Login to LinkedIn
        if not await agent.login_to_linkedin():
            return {"error": "Failed to login to LinkedIn"}
        
        # Search for jobs
        jobs = await agent.search_jobs(keyword, location)
        results["total_jobs_found"] = len(jobs)
        
        if not jobs:
            return {"error": "No jobs found"}
        
        # Analyze jobs
        for job in jobs[:max_jobs]:
            try:
                # AI analysis
                analysis = await agent.analyze_job_compatibility(job, resume_text)
                
                job_result = {
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "url": job["url"],
                    "similarity_score": 0.7,  # Placeholder
                    "ai_decision": "apply" if analysis["score"] >= 7 else "skip",
                    "ai_reason": analysis["reasoning"],
                    "ai_confidence": analysis["score"] / 10,
                    "application_status": "analyzed",
                    "application_reason": f"AI score: {analysis['score']}/10"
                }
                
                results["jobs"].append(job_result)
                results["jobs_analyzed"] += 1
                
            except Exception as e:
                error_msg = f"Error analyzing job {job['title']}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        # Generate summary
        results["summary"] = f"""
        AutoAgent Results:
        • Jobs Found: {results['total_jobs_found']}
        • Jobs Analyzed: {results['jobs_analyzed']}
        • High-scoring Jobs: {len([j for j in results['jobs'] if j.get('ai_confidence', 0) >= 0.7])}
        """
        
        logger.info("🎉 AutoAgent completed successfully")
        
    except Exception as e:
        error_msg = f"AutoAgent error: {str(e)}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
    
    finally:
        await agent.close_browser()
    
    return results