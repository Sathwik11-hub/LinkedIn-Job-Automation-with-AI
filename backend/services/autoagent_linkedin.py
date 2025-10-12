"""
AutoAgentHire - LinkedIn Job Automation Service
Robust implementation with proper Chromium browser handling.
"""
import os
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# PDF processing
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# AI processing
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

# Similarity processing
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    SIMILARITY_AVAILABLE = True
except ImportError:
    SIMILARITY_AVAILABLE = False

# Browser automation
try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoAgentLinkedIn:
    """
    AutoAgentHire LinkedIn automation service.
    Handles browser initialization, LinkedIn login, job search, and automated applications.
    """
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
        # Credentials
        self.linkedin_email = os.getenv("LINKEDIN_EMAIL")
        self.linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        
        # Initialize AI models
        self.gemini_model = None
        self.similarity_model = None
        
        self._initialize_ai_models()
    
    def _initialize_ai_models(self):
        """Initialize AI models for job analysis."""
        # Initialize Gemini AI
        if GENAI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
            try:
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
                logger.info("✅ Gemini AI initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Gemini AI: {e}")
        
        # Initialize similarity model
        if SIMILARITY_AVAILABLE:
            try:
                self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Similarity model initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize similarity model: {e}")
    
    def initialize_browser(self, headless: bool = False) -> bool:
        """
        Initialize Playwright Chromium browser.
        
        Args:
            headless: Whether to run browser in headless mode
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PLAYWRIGHT_AVAILABLE:
            logger.error("❌ Playwright not available. Install with: pip install playwright")
            return False
        
        try:
            # Start Playwright
            self.playwright = sync_playwright().start()
            
            # Enhanced browser arguments for better compatibility
            browser_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--disable-web-security',
                '--disable-features=TranslateUI',
                '--no-first-run',
                '--no-default-browser-check',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            
            # Launch browser
            self.browser = self.playwright.chromium.launch(
                headless=headless,
                args=browser_args,
                slow_mo=1000 if not headless else 0  # Slow down for visibility
            )
            
            # Create context with realistic settings
            context = self.browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1366, 'height': 768},
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            # Create page
            self.page = context.new_page()
            
            # Add stealth scripts
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            logger.info("🤖 Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize browser: {str(e)}")
            return False
    
    def login_to_linkedin(self) -> bool:
        """
        Login to LinkedIn using stored credentials.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        if not self.page:
            logger.error("❌ Browser not initialized")
            return False
        
        if not self.linkedin_email or not self.linkedin_password:
            logger.error("❌ LinkedIn credentials not found in environment variables")
            return False
        
        try:
            logger.info("🔐 Logging into LinkedIn...")
            
            # Navigate to login page
            self.page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            self.page.wait_for_timeout(2000)
            
            # Check if already logged in
            current_url = self.page.url
            if any(indicator in current_url for indicator in ["feed", "in/", "home"]):
                logger.info("✅ Already logged into LinkedIn")
                return True
            
            # Fill credentials
            email_field = self.page.locator('input[name="session_key"]')
            password_field = self.page.locator('input[name="session_password"]')
            submit_button = self.page.locator('button[type="submit"]')
            
            # Enter email
            email_field.fill(self.linkedin_email)
            self.page.wait_for_timeout(500)
            
            # Enter password
            password_field.fill(self.linkedin_password)
            self.page.wait_for_timeout(500)
            
            # Submit login
            submit_button.click()
            self.page.wait_for_timeout(5000)
            
            # Check login success
            current_url = self.page.url
            if any(indicator in current_url for indicator in ["feed", "in/", "home"]):
                logger.info("✅ LinkedIn login successful")
                return True
            elif "challenge" in current_url or "checkpoint" in current_url:
                logger.warning("⚠️ LinkedIn verification required - Please complete manually")
                # Wait for manual verification
                self.page.wait_for_timeout(30000)  # 30 seconds
                return True
            else:
                logger.error(f"❌ LinkedIn login failed - Current URL: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"❌ LinkedIn login error: {str(e)}")
            return False
    
    def extract_resume_text(self, resume_path: str) -> str:
        """
        Extract text from PDF resume.
        
        Args:
            resume_path: Path to the PDF resume file
            
        Returns:
            str: Extracted text from resume
        """
        if not PDF_AVAILABLE:
            logger.warning("⚠️ PyMuPDF not available. Cannot extract PDF text.")
            return ""
        
        try:
            doc = fitz.open(resume_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
            logger.info(f"📄 Extracted {len(text)} characters from resume")
            return text
            
        except Exception as e:
            logger.error(f"❌ Failed to extract resume text: {str(e)}")
            return ""
    
    def search_jobs(self, keyword: str, location: str = "", max_jobs: int = 10) -> List[Dict]:
        """
        Search for jobs on LinkedIn.
        
        Args:
            keyword: Job search keyword
            location: Job location
            max_jobs: Maximum number of jobs to return
            
        Returns:
            List[Dict]: List of job dictionaries
        """
        if not self.page:
            logger.error("❌ Browser not initialized")
            return []
        
        try:
            logger.info(f"🔍 Searching jobs: '{keyword}' in '{location}'")
            
            # Construct search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            if location:
                search_url += f"&location={location.replace(' ', '%20')}"
            search_url += "&f_AL=true"  # Easy Apply filter
            
            # Navigate to search results
            self.page.goto(search_url, wait_until="networkidle")
            self.page.wait_for_timeout(3000)
            
            # Extract job listings
            jobs = []
            job_cards = self.page.locator('.jobs-search-results__list-item').all()
            
            for i, job_card in enumerate(job_cards[:max_jobs]):
                try:
                    # Extract job details
                    title_element = job_card.locator('.base-search-card__title a')
                    company_element = job_card.locator('.base-search-card__subtitle')
                    location_element = job_card.locator('.job-search-card__location')
                    
                    # Get text content
                    title = title_element.inner_text() if title_element.count() > 0 else "Unknown Title"
                    company = company_element.inner_text() if company_element.count() > 0 else "Unknown Company"
                    job_location = location_element.inner_text() if location_element.count() > 0 else "Unknown Location"
                    
                    # Get job URL
                    job_url = ""
                    if title_element.count() > 0:
                        job_url = title_element.get_attribute('href') or ""
                        if job_url and not job_url.startswith('http'):
                            job_url = f"https://www.linkedin.com{job_url}"
                    
                    jobs.append({
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": job_location.strip(),
                        "url": job_url,
                        "index": i
                    })
                    
                except Exception as e:
                    logger.warning(f"⚠️ Error extracting job {i}: {str(e)}")
                    continue
            
            logger.info(f"📊 Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Job search error: {str(e)}")
            return []
    
    def analyze_job_compatibility(self, job: Dict, resume_text: str) -> Dict:
        """
        Analyze job compatibility using AI.
        
        Args:
            job: Job dictionary
            resume_text: Resume text content
            
        Returns:
            Dict: Analysis results with similarity score
        """
        try:
            # Use Gemini AI if available
            if self.gemini_model and resume_text:
                prompt = f"""
                Analyze the compatibility between this job and resume:
                
                JOB:
                Title: {job.get('title', 'N/A')}
                Company: {job.get('company', 'N/A')}
                Location: {job.get('location', 'N/A')}
                
                RESUME:
                {resume_text[:2000]}  # Limit for API
                
                Provide a compatibility score from 0-100 and brief reasoning.
                Format: Score: XX - Reasoning: your analysis
                """
                
                try:
                    response = self.gemini_model.generate_content(prompt)
                    analysis_text = response.text
                    
                    # Extract score from response
                    score = 50  # Default score
                    if "Score:" in analysis_text:
                        score_part = analysis_text.split("Score:")[1].split("-")[0].strip()
                        try:
                            score = int(score_part)
                        except:
                            score = 50
                    
                    return {
                        "similarity_score": score,
                        "analysis": analysis_text,
                        "method": "gemini_ai"
                    }
                    
                except Exception as e:
                    logger.warning(f"⚠️ Gemini AI analysis failed: {e}")
            
            # Fallback to similarity model
            if self.similarity_model and resume_text:
                try:
                    job_text = f"{job.get('title', '')} {job.get('company', '')}"
                    
                    # Compute embeddings
                    job_embedding = self.similarity_model.encode([job_text])
                    resume_embedding = self.similarity_model.encode([resume_text[:1000]])
                    
                    # Calculate similarity
                    similarity = np.dot(job_embedding[0], resume_embedding[0]) / (
                        np.linalg.norm(job_embedding[0]) * np.linalg.norm(resume_embedding[0])
                    )
                    
                    score = int(similarity * 100)
                    
                    return {
                        "similarity_score": score,
                        "analysis": f"Semantic similarity score: {score}%",
                        "method": "sentence_transformer"
                    }
                    
                except Exception as e:
                    logger.warning(f"⚠️ Similarity analysis failed: {e}")
            
            # Basic fallback
            return {
                "similarity_score": 60,
                "analysis": "Basic compatibility assessment - AI models not available",
                "method": "fallback"
            }
            
        except Exception as e:
            logger.error(f"❌ Job analysis error: {str(e)}")
            return {
                "similarity_score": 0,
                "analysis": f"Analysis failed: {str(e)}",
                "method": "error"
            }
    
    def apply_to_job(self, job: Dict) -> bool:
        """
        Apply to a job (simplified for demo).
        
        Args:
            job: Job dictionary
            
        Returns:
            bool: True if application attempted, False otherwise
        """
        try:
            if not job.get('url'):
                logger.warning("⚠️ No job URL available")
                return False
            
            logger.info(f"📝 Attempting to apply to: {job['title']} at {job['company']}")
            
            # Navigate to job page
            self.page.goto(job['url'], wait_until="networkidle")
            self.page.wait_for_timeout(2000)
            
            # Look for Easy Apply button
            easy_apply_button = self.page.locator('button:has-text(\"Easy Apply\")')
            
            if easy_apply_button.count() > 0:
                logger.info("✅ Easy Apply button found - Application process started")
                # For demo purposes, we'll just log this without actually applying
                # easy_apply_button.click()
                return True
            else:
                logger.info("ℹ️ No Easy Apply button found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Application error: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up browser resources."""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("🧹 Browser cleanup completed")
        except Exception as e:
            logger.warning(f"⚠️ Cleanup warning: {str(e)}")


def run_autoagent(
    keyword: str,
    location: str = "",
    resume_path: str = "",
    max_jobs: int = 10,
    similarity_threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Main function to run the AutoAgentHire automation.
    
    Args:
        keyword: Job search keyword
        location: Job location
        resume_path: Path to resume PDF file
        max_jobs: Maximum number of jobs to process
        similarity_threshold: Minimum similarity score for applications
        
    Returns:
        Dict: Results of the automation process
    """
    agent = AutoAgentLinkedIn()
    results = {
        "status": "started",
        "timestamp": time.time(),
        "jobs_found": 0,
        "jobs_analyzed": 0,
        "applications_attempted": 0,
        "successful_applications": 0,
        "jobs": [],
        "errors": []
    }
    
    try:
        # Step 1: Initialize browser
        logger.info("🚀 Starting AutoAgentHire automation...")
        if not agent.initialize_browser(headless=False):  # Non-headless for visibility
            return {"error": "Failed to initialize browser"}
        
        # Step 2: Login to LinkedIn
        if not agent.login_to_linkedin():
            return {"error": "Failed to login to LinkedIn"}
        
        # Step 3: Extract resume text
        resume_text = ""
        if resume_path and os.path.exists(resume_path):
            resume_text = agent.extract_resume_text(resume_path)
        
        # Step 4: Search for jobs
        jobs = agent.search_jobs(keyword, location, max_jobs)
        results["jobs_found"] = len(jobs)
        
        if not jobs:
            return {"error": "No jobs found for the given criteria"}
        
        # Step 5: Analyze and apply to jobs
        for job in jobs:
            try:
                # Analyze job compatibility
                analysis = agent.analyze_job_compatibility(job, resume_text)
                job["analysis"] = analysis
                results["jobs_analyzed"] += 1
                
                # Apply if meets threshold
                similarity_score = analysis.get("similarity_score", 0) / 100.0
                
                if similarity_score >= similarity_threshold:
                    logger.info(f"✅ Job meets threshold ({similarity_score:.2f} >= {similarity_threshold})")
                    
                    # Attempt application
                    results["applications_attempted"] += 1
                    if agent.apply_to_job(job):
                        results["successful_applications"] += 1
                        job["applied"] = True
                    else:
                        job["applied"] = False
                else:
                    logger.info(f"❌ Job below threshold ({similarity_score:.2f} < {similarity_threshold})")
                    job["applied"] = False
                
                results["jobs"].append(job)
                
                # Add delay between applications
                time.sleep(2)
                
            except Exception as e:
                error_msg = f"Error processing job '{job.get('title', 'Unknown')}': {str(e)}"
                logger.error(f"❌ {error_msg}")
                results["errors"].append(error_msg)
        
        results["status"] = "completed"
        logger.info(f"🎉 Automation completed - {results['successful_applications']} applications attempted")
        
        return results
        
    except Exception as e:
        error_msg = f"Automation failed: {str(e)}"
        logger.error(f"❌ {error_msg}")
        results["status"] = "failed"
        results["errors"].append(error_msg)
        return results
        
    finally:
        # Always cleanup
        agent.cleanup()


def test_browser_setup() -> Dict[str, Any]:
    """
    Test browser setup without full automation.
    
    Returns:
        Dict: Test results
    """
    agent = AutoAgentLinkedIn()
    
    try:
        # Test browser initialization
        if agent.initialize_browser(headless=False):
            result = {
                "browser_init": "✅ Success",
                "playwright": "✅ Available",
                "chromium": "✅ Launched"
            }
            
            # Test basic navigation
            try:
                agent.page.goto("https://www.linkedin.com")
                result["navigation"] = "✅ Success"
            except Exception as e:
                result["navigation"] = f"❌ Failed: {str(e)}"
            
            agent.cleanup()
            return result
        else:
            return {"browser_init": "❌ Failed"}
            
    except Exception as e:
        return {"error": f"Test failed: {str(e)}"}


if __name__ == "__main__":
    # Test run
    test_result = test_browser_setup()
    print("Browser Test Results:", test_result)
import os
import asyncio
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# PDF processing
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# AI processing
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

# Similarity processing
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    SIMILARITY_AVAILABLE = True
except ImportError:
    SIMILARITY_AVAILABLE = False

# Browser automation
try:
    from playwright.sync_api import sync_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os
import time
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    import fitz  # PyMuPDF for PDF text extraction
except ImportError:
    fitz = None

import google.generativeai as genai
from playwright.async_api import async_playwright, Browser, Page
from sentence_transformers import SentenceTransformer, util
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class AutoAgentLinkedIn:
    """LinkedIn automation service with AI-powered job matching."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize Gemini AI
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.ai_model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.ai_model = None
            logger.warning("GEMINI_API_KEY not found - AI analysis disabled")
    
    def extract_resume_text(self, file_path: str) -> str:
        """Extract text from PDF resume."""
        if not fitz:
            logger.error("PyMuPDF not installed - cannot extract PDF text")
            return ""
        
        try:
            text = ""
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text("text")
            doc.close()
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting resume text: {str(e)}")
            return ""
    
    async def initialize_browser(self, headless: bool = False) -> bool:
        """Initialize Playwright browser with stealth features."""
        try:
            playwright = await async_playwright().start()
            
            # Enhanced browser args for stealth
            browser_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--disable-web-security',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=browser_args
            )
            
            # Create context with realistic settings
            context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1366, 'height': 768},
                locale='en-US',
                timezone_id='America/New_York'
            )
            
            # Add stealth scripts
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                window.chrome = { runtime: {} };
            """)
            
            self.page = await context.new_page()
            logger.info("🤖 Browser initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {str(e)}")
            return False
    
    async def login_to_linkedin(self) -> bool:
        """Login to LinkedIn with enhanced security handling."""
        try:
            email = os.getenv("LINKEDIN_EMAIL")
            password = os.getenv("LINKEDIN_PASSWORD")
            
            if not (email and password):
                logger.error("LinkedIn credentials not found in environment variables")
                return False
            
            logger.info("🔐 Logging into LinkedIn...")
            
            # Navigate to login page
            await self.page.goto("https://www.linkedin.com/login", wait_until="networkidle")
            await self.page.wait_for_timeout(2000)
            
            # Fill credentials with human-like delays
            await self.page.fill('input[name="session_key"]', email)
            await self.page.wait_for_timeout(500)
            await self.page.fill('input[name="session_password"]', password)
            await self.page.wait_for_timeout(500)
            
            # Submit login
            await self.page.click('button[type="submit"]')
            await self.page.wait_for_timeout(5000)
            
            # Check if login was successful
            current_url = self.page.url
            if any(indicator in current_url for indicator in ["feed", "in/", "home"]):
                logger.info("✅ LinkedIn login successful")
                return True
            elif "challenge" in current_url or "checkpoint" in current_url:
                logger.warning("⚠️ LinkedIn verification required - manual intervention needed")
                # Wait for manual verification
                await self.page.wait_for_timeout(30000)
                current_url = self.page.url
                if any(indicator in current_url for indicator in ["feed", "in/", "home"]):
                    logger.info("✅ LinkedIn login successful after verification")
                    return True
                return False
            else:
                logger.error(f"❌ LinkedIn login failed - unexpected URL: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"LinkedIn login error: {str(e)}")
            return False
    
    async def search_jobs(self, keyword: str, location: str = "", max_jobs: int = 10) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn."""
        try:
            logger.info(f"🔍 Searching jobs: {keyword} in {location}")
            
            # Construct search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            if location:
                search_url += f"&location={location.replace(' ', '%20')}"
            search_url += "&f_AL=true"  # Easy Apply only
            
            await self.page.goto(search_url, wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            
            jobs = []
            job_elements = await self.page.query_selector_all('.jobs-search-results__list-item')
            
            for i, job_element in enumerate(job_elements[:max_jobs]):
                try:
                    # Extract job details
                    title_element = await job_element.query_selector('.base-search-card__title a')
                    company_element = await job_element.query_selector('.base-search-card__subtitle')
                    location_element = await job_element.query_selector('.job-search-card__location')
                    
                    title = await title_element.inner_text() if title_element else "Unknown Title"
                    company = await company_element.inner_text() if company_element else "Unknown Company"
                    job_location = await location_element.inner_text() if location_element else "Unknown Location"
                    job_link = await title_element.get_attribute('href') if title_element else ""
                    
                    if job_link and not job_link.startswith('http'):
                        job_link = f"https://www.linkedin.com{job_link}"
                    
                    jobs.append({
                        "title": title.strip(),
                        "company": company.strip(),
                        "location": job_location.strip(),
                        "url": job_link,
                        "index": i
                    })
                    
                except Exception as e:
                    logger.warning(f"Error extracting job {i}: {str(e)}")
                    continue
            
            logger.info(f"📊 Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Job search error: {str(e)}")
            return []
    
    def calculate_similarity(self, job_title: str, resume_text: str) -> float:
        """Calculate similarity between job and resume using sentence embeddings."""
        try:
            job_embedding = self.embedder.encode(job_title, convert_to_tensor=True)
            resume_embedding = self.embedder.encode(resume_text, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(job_embedding, resume_embedding).item()
            return similarity
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def ai_should_apply(self, job: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """Use Gemini AI to decide if we should apply to this job."""
        if not self.ai_model:
            return {"decision": "no", "reason": "AI model not available", "confidence": 0.0}
        
        try:
            prompt = f"""
            Job Title: {job['title']}
            Company: {job['company']}
            Location: {job['location']}
            
            Resume Summary: {resume_text[:800]}
            
            Should I apply to this job? Consider:
            1. Relevance to resume skills and experience
            2. Job title match with background
            3. Company reputation and growth potential
            
            Respond with:
            - Decision: yes/no
            - Reason: Brief explanation (max 100 words)
            - Confidence: 0.0-1.0 score
            
            Format: Decision: [yes/no] | Reason: [explanation] | Confidence: [score]
            """
            
            response = self.ai_model.generate_content(prompt)
            ai_response = response.text.lower()
            
            # Parse AI response
            decision = "yes" if "decision: yes" in ai_response else "no"
            
            reason_start = ai_response.find("reason:") + 7
            reason_end = ai_response.find("confidence:")
            reason = ai_response[reason_start:reason_end].strip() if reason_start > 6 else "AI analysis completed"
            
            confidence_start = ai_response.find("confidence:") + 11
            try:
                confidence = float(ai_response[confidence_start:confidence_start+3])
            except:
                confidence = 0.5
            
            return {
                "decision": decision,
                "reason": reason[:200],  # Limit reason length
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"AI analysis error: {str(e)}")
            return {"decision": "no", "reason": f"AI error: {str(e)}", "confidence": 0.0}
    
    async def apply_to_job(self, job: Dict[str, Any], resume_path: str) -> Dict[str, Any]:
        """Apply to a specific job if Easy Apply is available."""
        try:
            logger.info(f"📝 Attempting to apply to: {job['title']} at {job['company']}")
            
            # Navigate to job page
            await self.page.goto(job['url'], wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Look for Easy Apply button
            easy_apply_button = await self.page.query_selector('button:has-text("Easy Apply")')
            if not easy_apply_button:
                return {"status": "skipped", "reason": "No Easy Apply button found"}
            
            # Click Easy Apply
            await easy_apply_button.click()
            await self.page.wait_for_timeout(2000)
            
            # Handle file upload if resume input is found
            file_input = await self.page.query_selector('input[type="file"]')
            if file_input and os.path.exists(resume_path):
                await file_input.set_input_files(resume_path)
                await self.page.wait_for_timeout(1000)
            
            # Look for submit button - try multiple selectors
            submit_selectors = [
                'button:has-text("Submit application")',
                'button:has-text("Submit")',
                'button[type="submit"]',
                'button.artdeco-button--primary'
            ]
            
            submitted = False
            for selector in submit_selectors:
                submit_button = await self.page.query_selector(selector)
                if submit_button:
                    await submit_button.click()
                    await self.page.wait_for_timeout(2000)
                    submitted = True
                    break
            
            if submitted:
                logger.info(f"✅ Successfully applied to {job['title']}")
                return {"status": "applied", "reason": "Application submitted successfully"}
            else:
                return {"status": "partial", "reason": "Application started but may need manual completion"}
                
        except Exception as e:
            logger.error(f"Error applying to job: {str(e)}")
            return {"status": "error", "reason": f"Application error: {str(e)}"}
    
    async def close_browser(self):
        """Close the browser and clean up resources."""
        if self.browser:
            await self.browser.close()
            logger.info("🧹 Browser closed")


async def run_autoagent(keyword: str, location: str, resume_path: str, max_jobs: int = 10, similarity_threshold: float = 0.5) -> Dict[str, Any]:
    """
    Main function to run the AutoAgent LinkedIn automation.
    
    Args:
        keyword: Job search keyword
        location: Job location
        resume_path: Path to resume PDF file
        max_jobs: Maximum number of jobs to process
        similarity_threshold: Minimum similarity score to consider applying
    
    Returns:
        Dictionary with automation results
    """
    # Validate environment variables
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not (email and password):
        return {"error": "Missing LinkedIn credentials in environment variables"}
    
    if not gemini_key:
        logger.warning("GEMINI_API_KEY not found - AI analysis will be limited")
    
    # Validate resume file
    if not os.path.exists(resume_path):
        return {"error": f"Resume file not found: {resume_path}"}
    
    agent = AutoAgentLinkedIn()
    results = {
        "total_jobs_found": 0,
        "jobs_analyzed": 0,
        "applications_attempted": 0,
        "applications_successful": 0,
        "applications_failed": 0,
        "jobs": [],
        "summary": "",
        "errors": []
    }
    
    try:
        # Extract resume text
        resume_text = agent.extract_resume_text(resume_path)
        if not resume_text:
            return {"error": "Could not extract text from resume PDF"}
        
        # Initialize browser
        if not await agent.initialize_browser(headless=False):  # Visible for demo
            return {"error": "Failed to initialize browser"}
        
        # Login to LinkedIn
        if not await agent.login_to_linkedin():
            return {"error": "Failed to login to LinkedIn"}
        
        # Search for jobs
        jobs = await agent.search_jobs(keyword, location, max_jobs)
        results["total_jobs_found"] = len(jobs)
        
        if not jobs:
            return {"error": "No jobs found for the given criteria"}
        
        # Process each job
        for job in jobs:
            try:
                # Calculate similarity
                similarity = agent.calculate_similarity(job['title'], resume_text)
                
                # Get AI decision
                ai_decision = agent.ai_should_apply(job, resume_text)
                
                job_result = {
                    "title": job['title'],
                    "company": job['company'],
                    "location": job['location'],
                    "url": job['url'],
                    "similarity_score": round(similarity, 3),
                    "ai_decision": ai_decision['decision'],
                    "ai_reason": ai_decision['reason'],
                    "ai_confidence": ai_decision['confidence'],
                    "application_status": "not_attempted",
                    "application_reason": ""
                }
                
                results["jobs_analyzed"] += 1
                
                # Decide whether to apply
                should_apply = (
                    ai_decision['decision'] == 'yes' and 
                    similarity > similarity_threshold and
                    ai_decision['confidence'] > 0.6
                )
                
                if should_apply:
                    results["applications_attempted"] += 1
                    application_result = await agent.apply_to_job(job, resume_path)
                    
                    job_result["application_status"] = application_result["status"]
                    job_result["application_reason"] = application_result["reason"]
                    
                    if application_result["status"] == "applied":
                        results["applications_successful"] += 1
                    else:
                        results["applications_failed"] += 1
                        
                    # Add delay between applications
                    await asyncio.sleep(5)
                else:
                    job_result["application_status"] = "skipped"
                    job_result["application_reason"] = f"Low similarity ({similarity:.2f}) or AI confidence ({ai_decision['confidence']:.2f})"
                
                results["jobs"].append(job_result)
                
            except Exception as e:
                error_msg = f"Error processing job {job['title']}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
        
        # Generate summary
        results["summary"] = f"""
        AutoAgent LinkedIn Automation Summary:
        • Jobs Found: {results['total_jobs_found']}
        • Jobs Analyzed: {results['jobs_analyzed']}
        • Applications Attempted: {results['applications_attempted']}
        • Applications Successful: {results['applications_successful']}
        • Applications Failed: {results['applications_failed']}
        • Success Rate: {(results['applications_successful'] / max(1, results['applications_attempted']) * 100):.1f}%
        """
        
        logger.info("🎉 AutoAgent automation completed successfully")
        
    except Exception as e:
        error_msg = f"AutoAgent automation error: {str(e)}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
        
    finally:
        # Cleanup
        await agent.close_browser()
    
    return results