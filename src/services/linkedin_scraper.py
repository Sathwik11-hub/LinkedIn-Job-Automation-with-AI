"""LinkedIn scraper service using Selenium."""

import time
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from ..core import LoggerMixin, get_settings
from ..models import JobPosting, JobSearchFilters, JobExperienceLevel


class LinkedInScraper(LoggerMixin):
    """LinkedIn job scraper using Selenium."""
    
    def __init__(self):
        self.settings = get_settings()
        self.driver: Optional[webdriver.Chrome] = None
        self.is_logged_in = False
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        if not self.settings.debug:
            chrome_options.add_argument("--headless")
            
        # User agent to avoid detection
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=chrome_options
        )
        
        # Execute script to hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.driver = self._setup_driver()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.driver:
            self.driver.quit()
    
    def login(self) -> bool:
        """Login to LinkedIn."""
        try:
            self.logger.info("Attempting to login to LinkedIn")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            wait = WebDriverWait(self.driver, 10)
            
            # Enter email
            email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_field.send_keys(self.settings.linkedin_email)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.settings.linkedin_password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for redirect to feed or handle 2FA
            time.sleep(5)
            
            # Check if we're logged in
            current_url = self.driver.current_url
            if "feed" in current_url or "in/" in current_url:
                self.is_logged_in = True
                self.logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                self.logger.error("Failed to login to LinkedIn")
                return False
                
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False
    
    def search_jobs(self, filters: JobSearchFilters) -> List[JobPosting]:
        """Search for jobs based on filters."""
        if not self.is_logged_in:
            if not self.login():
                raise Exception("Failed to login to LinkedIn")
        
        jobs = []
        try:
            self.logger.info(f"Searching jobs with keywords: {filters.keywords}")
            
            # Build search URL
            search_params = {
                "keywords": filters.keywords,
                "location": filters.location,
                "f_TPR": self._get_date_filter(filters.date_posted),
                "f_E": self._get_experience_filter(filters.experience_level),
                "f_JT": self._get_job_type_filter(filters.job_type),
                "f_WT": "2" if filters.remote_only else None,  # Remote work
            }
            
            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}
            
            search_url = f"https://www.linkedin.com/jobs/search/?{urlencode(search_params)}"
            self.driver.get(search_url)
            
            time.sleep(3)
            
            # Scroll to load more jobs
            self._scroll_to_load_jobs(filters.max_results)
            
            # Extract job listings
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
            
            for card in job_cards[:filters.max_results]:
                try:
                    job = self._extract_job_from_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    self.logger.warning(f"Failed to extract job from card: {str(e)}")
                    continue
            
            self.logger.info(f"Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Job search failed: {str(e)}")
            raise
    
    def _get_date_filter(self, date_posted: Optional[str]) -> Optional[str]:
        """Convert date filter to LinkedIn format."""
        date_map = {
            "past_24_hours": "r86400",
            "past_week": "r604800",
            "past_month": "r2592000"
        }
        return date_map.get(date_posted)
    
    def _get_experience_filter(self, experience_level: Optional[JobExperienceLevel]) -> Optional[str]:
        """Convert experience level to LinkedIn format."""
        if not experience_level:
            return None
            
        experience_map = {
            JobExperienceLevel.INTERNSHIP: "1",
            JobExperienceLevel.ENTRY_LEVEL: "2",
            JobExperienceLevel.ASSOCIATE: "3",
            JobExperienceLevel.MID_SENIOR: "4",
            JobExperienceLevel.DIRECTOR: "5",
            JobExperienceLevel.EXECUTIVE: "6"
        }
        return experience_map.get(experience_level)
    
    def _get_job_type_filter(self, job_type: Optional[str]) -> Optional[str]:
        """Convert job type to LinkedIn format."""
        if not job_type:
            return None
            
        job_type_map = {
            "full_time": "F",
            "part_time": "P",
            "contract": "C",
            "temporary": "T",
            "internship": "I"
        }
        return job_type_map.get(job_type.lower())
    
    def _scroll_to_load_jobs(self, max_results: int):
        """Scroll down to load more job listings."""
        current_jobs = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while current_jobs < max_results:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Check if more jobs loaded
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
                
            last_height = new_height
            current_jobs = len(self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card"))
    
    def _extract_job_from_card(self, card) -> Optional[JobPosting]:
        """Extract job information from a job card element."""
        try:
            # Job title and URL
            title_element = card.find_element(By.CSS_SELECTOR, ".job-search-card__title a")
            title = title_element.text.strip()
            job_url = title_element.get_attribute("href")
            
            # Extract job ID from URL
            job_id_match = re.search(r"jobs/view/(\d+)", job_url)
            job_id = job_id_match.group(1) if job_id_match else None
            
            if not job_id:
                return None
            
            # Company name
            company_element = card.find_element(By.CSS_SELECTOR, ".job-search-card__subtitle a")
            company = company_element.text.strip()
            
            # Location
            location_element = card.find_element(By.CSS_SELECTOR, ".job-search-card__location")
            location = location_element.text.strip()
            
            # Posted date
            posted_date = None
            try:
                date_element = card.find_element(By.CSS_SELECTOR, ".job-search-card__listdate")
                posted_date_text = date_element.get_attribute("datetime")
                if posted_date_text:
                    posted_date = datetime.fromisoformat(posted_date_text.replace("Z", "+00:00"))
            except NoSuchElementException:
                pass
            
            # Get full job description
            description = self._get_job_description(job_url)
            
            return JobPosting(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                description=description,
                url=job_url,
                posted_date=posted_date
            )
            
        except Exception as e:
            self.logger.warning(f"Failed to extract job data: {str(e)}")
            return None
    
    def _get_job_description(self, job_url: str) -> str:
        """Get full job description from job page."""
        try:
            # Store current window handle
            original_window = self.driver.current_window_handle
            
            # Open job in new tab
            self.driver.execute_script(f"window.open('{job_url}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Wait for job description to load
            wait = WebDriverWait(self.driver, 10)
            description_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".description__text"))
            )
            
            description = description_element.text.strip()
            
            # Close tab and switch back
            self.driver.close()
            self.driver.switch_to.window(original_window)
            
            return description
            
        except Exception as e:
            self.logger.warning(f"Failed to get job description: {str(e)}")
            # Close any open tabs and switch back
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            return "Description not available"