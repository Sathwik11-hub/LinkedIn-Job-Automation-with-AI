"""
LinkedIn job scraping service using Selenium/Playwright
"""

import asyncio
import re
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from app.models.job_schema import Job, JobType, ExperienceLevel
from app.config import settings
from app.utils.logger import setup_logger, log_async_performance

logger = setup_logger(__name__)


class JobScraper:
    """
    LinkedIn job scraper using Selenium
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.logged_in = False
        
    def _setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            
            if settings.headless_browser:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("Chrome driver setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            raise
    
    async def _login_to_linkedin(self):
        """Login to LinkedIn using credentials"""
        if not settings.linkedin_email or not settings.linkedin_password:
            logger.warning("LinkedIn credentials not provided, scraping without login")
            return False
        
        try:
            logger.info("Logging into LinkedIn...")
            
            # Navigate to LinkedIn login
            self.driver.get("https://www.linkedin.com/login")
            await asyncio.sleep(2)
            
            # Enter credentials
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            password_field = self.driver.find_element(By.ID, "password")
            
            email_field.send_keys(settings.linkedin_email)
            password_field.send_keys(settings.linkedin_password)
            
            # Submit login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            await asyncio.sleep(5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "home" in self.driver.current_url:
                self.logged_in = True
                logger.info("Successfully logged into LinkedIn")
                return True
            else:
                logger.warning("LinkedIn login may have failed")
                return False
                
        except Exception as e:
            logger.error(f"Error logging into LinkedIn: {e}")
            return False
    
    @log_async_performance
    async def search_jobs(
        self,
        keywords: str,
        location: str = "United States",
        job_type: Optional[JobType] = None,
        experience_level: Optional[ExperienceLevel] = None,
        limit: int = 50
    ) -> List[Job]:
        """
        Search for jobs on LinkedIn
        
        Args:
            keywords: Search keywords
            location: Job location
            job_type: Job type filter
            experience_level: Experience level filter
            limit: Maximum number of jobs to return
            
        Returns:
            List of Job objects
        """
        jobs = []
        
        try:
            # Setup driver if not already done
            if not self.driver:
                self._setup_driver()
                await self._login_to_linkedin()
            
            # Build search URL
            search_url = self._build_search_url(keywords, location, job_type, experience_level)
            logger.info(f"Searching jobs with URL: {search_url}")
            
            # Navigate to search results
            self.driver.get(search_url)
            await asyncio.sleep(3)
            
            # Scroll and collect job listings
            collected_jobs = 0
            page_num = 0
            
            while collected_jobs < limit:
                # Get job cards on current page
                job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-entity-urn*='urn:li:jobPosting:']")
                
                if not job_cards:
                    logger.warning("No job cards found on current page")
                    break
                
                # Process each job card
                for card in job_cards:
                    if collected_jobs >= limit:
                        break
                    
                    try:
                        job = await self._extract_job_from_card(card)
                        if job:
                            jobs.append(job)
                            collected_jobs += 1
                            logger.debug(f"Extracted job: {job.title} at {job.company}")
                    
                    except Exception as e:
                        logger.warning(f"Error extracting job from card: {e}")
                        continue
                
                # Try to go to next page
                if collected_jobs < limit:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Next']")
                        if next_button.is_enabled():
                            next_button.click()
                            await asyncio.sleep(3)
                            page_num += 1
                        else:
                            break
                    except NoSuchElementException:
                        logger.info("No more pages available")
                        break
            
            logger.info(f"Successfully scraped {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error searching jobs: {e}")
            return jobs
        
        finally:
            # Don't close driver here, reuse for efficiency
            pass
    
    async def get_job_details(self, job_id: str) -> Optional[Job]:
        """
        Get detailed information about a specific job
        
        Args:
            job_id: LinkedIn job ID
            
        Returns:
            Job object with detailed information
        """
        try:
            # Setup driver if not already done
            if not self.driver:
                self._setup_driver()
                await self._login_to_linkedin()
            
            # Navigate to job details page
            job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
            self.driver.get(job_url)
            await asyncio.sleep(3)
            
            # Extract detailed job information
            job = await self._extract_detailed_job()
            
            if job:
                job.id = job_id
                job.linkedin_url = job_url
            
            return job
            
        except Exception as e:
            logger.error(f"Error getting job details for {job_id}: {e}")
            return None
    
    def _build_search_url(
        self,
        keywords: str,
        location: str,
        job_type: Optional[JobType] = None,
        experience_level: Optional[ExperienceLevel] = None
    ) -> str:
        """Build LinkedIn job search URL"""
        
        base_url = "https://www.linkedin.com/jobs/search/?"
        params = []
        
        # Keywords
        params.append(f"keywords={quote(keywords)}")
        
        # Location
        params.append(f"location={quote(location)}")
        
        # Job type mapping
        if job_type:
            job_type_map = {
                JobType.FULL_TIME: "F",
                JobType.PART_TIME: "P",
                JobType.CONTRACT: "C",
                JobType.INTERNSHIP: "I",
                JobType.TEMPORARY: "T"
            }
            if job_type in job_type_map:
                params.append(f"f_JT={job_type_map[job_type]}")
        
        # Experience level mapping
        if experience_level:
            exp_level_map = {
                ExperienceLevel.ENTRY_LEVEL: "1",
                ExperienceLevel.ASSOCIATE: "2",
                ExperienceLevel.MID_SENIOR: "3",
                ExperienceLevel.DIRECTOR: "4",
                ExperienceLevel.EXECUTIVE: "5"
            }
            if experience_level in exp_level_map:
                params.append(f"f_E={exp_level_map[experience_level]}")
        
        # Additional filters
        params.append("f_TPR=r86400")  # Posted in last 24 hours
        params.append("sortBy=DD")  # Sort by date
        
        return base_url + "&".join(params)
    
    async def _extract_job_from_card(self, card_element) -> Optional[Job]:
        """Extract job information from a job card element"""
        try:
            # Extract basic information
            title_element = card_element.find_element(By.CSS_SELECTOR, "h3 a")
            title = title_element.text.strip()
            job_url = title_element.get_attribute("href")
            
            # Extract job ID from URL
            job_id_match = re.search(r'/jobs/view/(\d+)', job_url)
            job_id = job_id_match.group(1) if job_id_match else "unknown"
            
            # Company name
            company_element = card_element.find_element(By.CSS_SELECTOR, "h4 a")
            company = company_element.text.strip()
            
            # Location
            try:
                location_element = card_element.find_element(By.CSS_SELECTOR, "[data-test-id='job-search-card-location']")
                location = location_element.text.strip()
            except NoSuchElementException:
                location = "Not specified"
            
            # Posted date
            try:
                time_element = card_element.find_element(By.CSS_SELECTOR, "time")
                posted_date_str = time_element.get_attribute("datetime")
                posted_date = datetime.fromisoformat(posted_date_str.replace('Z', '+00:00'))
            except:
                posted_date = datetime.utcnow()
            
            # Create Job object
            job = Job(
                id=job_id,
                title=title,
                company=company,
                location=location,
                job_type=JobType.FULL_TIME,  # Default, can be refined
                experience_level=ExperienceLevel.MID_SENIOR,  # Default, can be refined
                description="",  # Will be filled by detailed scraping
                requirements=[],
                skills=[],
                benefits=[],
                posted_date=posted_date,
                linkedin_url=job_url
            )
            
            return job
            
        except Exception as e:
            logger.warning(f"Error extracting job from card: {e}")
            return None
    
    async def _extract_detailed_job(self) -> Optional[Job]:
        """Extract detailed job information from job details page"""
        try:
            # This is a simplified version - full implementation would extract
            # detailed description, requirements, skills, etc.
            
            # Basic info
            title = self.driver.find_element(By.CSS_SELECTOR, "h1").text.strip()
            
            try:
                company = self.driver.find_element(By.CSS_SELECTOR, ".topcard__org-name-link").text.strip()
            except:
                company = "Unknown Company"
            
            try:
                location = self.driver.find_element(By.CSS_SELECTOR, ".topcard__flavor--bullet").text.strip()
            except:
                location = "Not specified"
            
            # Description
            try:
                description_element = self.driver.find_element(By.CSS_SELECTOR, ".description__text")
                description = description_element.text.strip()
            except:
                description = "No description available"
            
            job = Job(
                id="",  # Will be set by caller
                title=title,
                company=company,
                location=location,
                job_type=JobType.FULL_TIME,
                experience_level=ExperienceLevel.MID_SENIOR,
                description=description,
                requirements=[],
                skills=[],
                benefits=[],
                linkedin_url=""  # Will be set by caller
            )
            
            return job
            
        except Exception as e:
            logger.error(f"Error extracting detailed job: {e}")
            return None
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Browser driver closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()