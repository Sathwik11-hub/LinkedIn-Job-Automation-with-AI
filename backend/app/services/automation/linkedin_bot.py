from playwright.async_api import async_playwright, Browser, Page, BrowserContext
import asyncio
from typing import List, Dict, Optional, Tuple
from app.core.config import settings
import time
import random

class LinkedInBot:
    def __init__(self, credentials: Dict[str, str]):
        self.email = credentials.get("email", settings.linkedin_email)
        self.password = credentials.get("password", settings.linkedin_password)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
    
    async def start_browser(self):
        """Initialize the browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=settings.headless_browser,
            args=['--disable-blink-features=AutomationControlled'],
            slow_mo=1000  # Slow down operations
        )
        
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        self.page = await self.context.new_page()
        
        # Add stealth settings
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
    
    async def login(self) -> bool:
        """Login to LinkedIn"""
        if not self.page:
            await self.start_browser()
        
        try:
            # Navigate to LinkedIn login
            await self.page.goto("https://www.linkedin.com/login", timeout=settings.browser_timeout)
            await self._random_delay(2, 4)
            
            # Fill login form
            await self.page.fill("#username", self.email)
            await self._random_delay(1, 2)
            await self.page.fill("#password", self.password)
            await self._random_delay(1, 2)
            
            # Click login button
            await self.page.click("[type='submit']")
            await self._random_delay(3, 5)
            
            # Check if login was successful
            if await self._verify_login():
                self.is_logged_in = True
                print("Successfully logged in to LinkedIn")
                return True
            else:
                print("Login failed or requires additional verification")
                return False
                
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    async def search_jobs(
        self, 
        keywords: str, 
        location: str = "", 
        job_type: str = "", 
        experience_level: str = ""
    ) -> List[Dict]:
        """Search for jobs on LinkedIn"""
        if not self.is_logged_in:
            if not await self.login():
                return []
        
        jobs = []
        
        try:
            # Navigate to jobs page
            await self.page.goto("https://www.linkedin.com/jobs/", timeout=settings.browser_timeout)
            await self._random_delay(2, 4)
            
            # Search for jobs
            search_box = await self.page.wait_for_selector("input[aria-label*='Search jobs']", timeout=10000)
            await search_box.fill(keywords)
            await self._random_delay(1, 2)
            
            # Add location if provided
            if location:
                location_box = await self.page.wait_for_selector("input[aria-label*='City']", timeout=5000)
                await location_box.fill(location)
                await self._random_delay(1, 2)
            
            # Submit search
            await self.page.keyboard.press("Enter")
            await self._random_delay(3, 5)
            
            # Extract job listings
            jobs = await self._extract_job_listings()
            
        except Exception as e:
            print(f"Error searching jobs: {e}")
        
        return jobs
    
    async def apply_to_job(self, job_url: str, cover_letter: str = "") -> Dict:
        """Apply to a specific job"""
        if not self.is_logged_in:
            if not await self.login():
                return {"success": False, "error": "Not logged in"}
        
        try:
            # Navigate to job page
            await self.page.goto(job_url, timeout=settings.browser_timeout)
            await self._random_delay(2, 4)
            
            # Look for Easy Apply button
            easy_apply_button = await self.page.query_selector("button[aria-label*='Easy Apply']")
            
            if not easy_apply_button:
                return {"success": False, "error": "Easy Apply not available"}
            
            # Click Easy Apply
            await easy_apply_button.click()
            await self._random_delay(2, 4)
            
            # Handle application process
            result = await self._handle_application_flow(cover_letter)
            return result
            
        except Exception as e:
            print(f"Error applying to job: {e}")
            return {"success": False, "error": str(e)}
    
    async def _verify_login(self) -> bool:
        """Verify if login was successful"""
        try:
            # Check for feed or profile indicators
            await self.page.wait_for_selector("nav[aria-label='Primary Navigation']", timeout=10000)
            return True
        except:
            # Check if we're on a verification page
            if "challenge" in self.page.url or "checkpoint" in self.page.url:
                print("Login requires additional verification (CAPTCHA/2FA)")
                # In a real implementation, you'd handle this appropriately
                return False
            return False
    
    async def _extract_job_listings(self) -> List[Dict]:
        """Extract job listings from search results"""
        jobs = []
        
        try:
            # Wait for job listings to load
            await self.page.wait_for_selector("li[data-occludable-job-id]", timeout=10000)
            
            # Get job cards
            job_cards = await self.page.query_selector_all("li[data-occludable-job-id]")
            
            for i, card in enumerate(job_cards[:10]):  # Limit to first 10 jobs
                try:
                    # Extract job information
                    job_data = await self._extract_job_data(card)
                    if job_data:
                        jobs.append(job_data)
                        
                    await self._random_delay(0.5, 1.5)
                    
                except Exception as e:
                    print(f"Error extracting job {i}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error extracting job listings: {e}")
        
        return jobs
    
    async def _extract_job_data(self, job_card) -> Optional[Dict]:
        """Extract data from a single job card"""
        try:
            # Job title
            title_element = await job_card.query_selector("h3 a")
            title = await title_element.inner_text() if title_element else "Unknown"
            
            # Job URL
            job_url = await title_element.get_attribute("href") if title_element else ""
            if job_url and not job_url.startswith("http"):
                job_url = "https://www.linkedin.com" + job_url
            
            # Company name
            company_element = await job_card.query_selector("h4 a")
            company = await company_element.inner_text() if company_element else "Unknown"
            
            # Location
            location_element = await job_card.query_selector("div[class*='job-search-card__location']")
            location = await location_element.inner_text() if location_element else "Unknown"
            
            # Posted time
            time_element = await job_card.query_selector("time")
            posted_time = await time_element.get_attribute("datetime") if time_element else ""
            
            return {
                "title": title.strip(),
                "company": company.strip(),
                "location": location.strip(),
                "job_url": job_url,
                "posted_time": posted_time,
                "linkedin_job_id": self._extract_job_id(job_url)
            }
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    async def _handle_application_flow(self, cover_letter: str) -> Dict:
        """Handle the Easy Apply application flow"""
        try:
            # This is a simplified version - real implementation would be more complex
            # Look for submit button or next button
            submit_button = await self.page.query_selector("button[aria-label*='Submit'], button[aria-label*='Review']")
            
            if submit_button:
                # If there's a cover letter field, fill it
                cover_letter_field = await self.page.query_selector("textarea")
                if cover_letter_field and cover_letter:
                    await cover_letter_field.fill(cover_letter)
                    await self._random_delay(1, 2)
                
                await submit_button.click()
                await self._random_delay(2, 4)
                
                return {"success": True, "message": "Application submitted"}
            else:
                return {"success": False, "error": "Could not find submit button"}
                
        except Exception as e:
            return {"success": False, "error": f"Application flow error: {e}"}
    
    def _extract_job_id(self, job_url: str) -> str:
        """Extract LinkedIn job ID from URL"""
        import re
        match = re.search(r'/jobs/view/(\d+)', job_url)
        return match.group(1) if match else ""
    
    async def _random_delay(self, min_seconds: float, max_seconds: float):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def close(self):
        """Close the browser"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None
            self.page = None
            self.is_logged_in = False