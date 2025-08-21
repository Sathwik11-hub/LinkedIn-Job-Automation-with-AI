"""
LinkedIn automation bot using Selenium
Handles login, job navigation, and application submission
"""

import asyncio
import random
from typing import Optional, Dict, Any
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    WebDriverException
)

from app.config import settings
from app.utils.logger import setup_logger, log_async_performance

logger = setup_logger(__name__)


class LinkedInBot:
    """
    LinkedIn automation bot for job applications
    """
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.logged_in = False
        self.current_job_url = None
        
        # Selectors for LinkedIn elements (these may need updates as LinkedIn changes)
        self.selectors = {
            'login': {
                'email': "input[name='session_key']",
                'password': "input[name='session_password']",
                'submit': "button[type='submit']"
            },
            'job': {
                'apply_button': "button[data-control-name='jobdetails_topcard_inapply']",
                'easy_apply_button': ".jobs-apply-button",
                'submit_button': "button[aria-label='Submit application']",
                'next_button': "button[aria-label='Continue to next step']",
                'review_button': "button[aria-label='Review your application']"
            },
            'form': {
                'file_input': "input[type='file']",
                'text_area': "textarea",
                'text_input': "input[type='text']",
                'radio_button': "input[type='radio']",
                'checkbox': "input[type='checkbox']",
                'select': "select"
            }
        }
    
    async def initialize(self):
        """Initialize the browser driver"""
        try:
            chrome_options = Options()
            
            # Configure Chrome options
            if settings.headless_browser:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            
            # User agent to appear more human-like
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("LinkedIn bot initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing LinkedIn bot: {e}")
            raise
    
    @log_async_performance
    async def login(self, email: str = None, password: str = None) -> bool:
        """
        Login to LinkedIn
        
        Args:
            email: LinkedIn email (uses config if not provided)
            password: LinkedIn password (uses config if not provided)
            
        Returns:
            True if login successful, False otherwise
        """
        if not self.driver:
            await self.initialize()
        
        email = email or settings.linkedin_email
        password = password or settings.linkedin_password
        
        if not email or not password:
            logger.error("LinkedIn credentials not provided")
            return False
        
        try:
            logger.info("Logging into LinkedIn...")
            
            # Navigate to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            await self._random_delay(1, 3)
            
            # Enter email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['login']['email']))
            )
            await self._human_type(email_field, email)
            
            # Enter password
            password_field = self.driver.find_element(By.CSS_SELECTOR, self.selectors['login']['password'])
            await self._human_type(password_field, password)
            
            # Submit login form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, self.selectors['login']['submit'])
            await self._human_click(submit_button)
            
            # Wait for login to complete
            await self._random_delay(3, 5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "home" in self.driver.current_url:
                self.logged_in = True
                logger.info("Successfully logged into LinkedIn")
                return True
            elif "challenge" in self.driver.current_url:
                logger.warning("LinkedIn security challenge detected - manual intervention may be required")
                return False
            else:
                logger.error("LinkedIn login failed")
                return False
                
        except Exception as e:
            logger.error(f"Error during LinkedIn login: {e}")
            return False
    
    def is_logged_in(self) -> bool:
        """Check if currently logged in to LinkedIn"""
        return self.logged_in and self.driver is not None
    
    async def navigate_to_job(self, job_url: str) -> bool:
        """
        Navigate to a specific job posting
        
        Args:
            job_url: LinkedIn job URL
            
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            logger.info(f"Navigating to job: {job_url}")
            
            self.driver.get(job_url)
            self.current_job_url = job_url
            await self._random_delay(2, 4)
            
            # Wait for job page to load
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                )
                logger.debug("Job page loaded successfully")
                return True
            except TimeoutException:
                logger.error("Job page failed to load")
                return False
                
        except Exception as e:
            logger.error(f"Error navigating to job: {e}")
            return False
    
    async def can_apply_to_job(self) -> bool:
        """
        Check if we can apply to the current job
        
        Returns:
            True if application is possible, False otherwise
        """
        try:
            # Look for apply button
            apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['job']['apply_button'])
            easy_apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['job']['easy_apply_button'])
            
            if apply_buttons or easy_apply_buttons:
                # Check if button is enabled and not showing "Applied"
                for button in apply_buttons + easy_apply_buttons:
                    button_text = button.text.lower()
                    if "apply" in button_text and "applied" not in button_text:
                        return True
            
            logger.warning("No applicable apply button found or already applied")
            return False
            
        except Exception as e:
            logger.error(f"Error checking if can apply to job: {e}")
            return False
    
    async def click_apply_button(self) -> bool:
        """
        Click the apply button on job page
        
        Returns:
            True if button clicked successfully, False otherwise
        """
        try:
            # Try Easy Apply first (preferred)
            easy_apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['job']['easy_apply_button'])
            
            for button in easy_apply_buttons:
                if "easy apply" in button.text.lower():
                    await self._human_click(button)
                    await self._random_delay(1, 2)
                    logger.info("Clicked Easy Apply button")
                    return True
            
            # Try regular apply button
            apply_buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['job']['apply_button'])
            
            for button in apply_buttons:
                if "apply" in button.text.lower() and "applied" not in button.text.lower():
                    await self._human_click(button)
                    await self._random_delay(1, 2)
                    logger.info("Clicked Apply button")
                    return True
            
            logger.error("No clickable apply button found")
            return False
            
        except Exception as e:
            logger.error(f"Error clicking apply button: {e}")
            return False
    
    @log_async_performance
    async def fill_application_form(
        self,
        resume_path: str,
        cover_letter: str = None,
        custom_message: str = None
    ) -> bool:
        """
        Fill out the job application form
        
        Args:
            resume_path: Path to resume file
            cover_letter: Cover letter text
            custom_message: Custom message for application
            
        Returns:
            True if form filled successfully, False otherwise
        """
        try:
            logger.info("Filling application form...")
            
            # Wait for form to load
            await self._random_delay(2, 3)
            
            # Upload resume if file input is present
            if await self._upload_resume(resume_path):
                logger.info("Resume uploaded successfully")
            
            # Fill text fields
            await self._fill_text_fields(cover_letter, custom_message)
            
            # Handle any additional form fields
            await self._handle_additional_fields()
            
            logger.info("Application form filled successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error filling application form: {e}")
            return False
    
    async def submit_application(self) -> bool:
        """
        Submit the job application
        
        Returns:
            True if submission successful, False otherwise
        """
        try:
            logger.info("Submitting application...")
            
            # Look for submit/send button
            submit_selectors = [
                "button[aria-label='Submit application']",
                "button[aria-label='Send application']",
                "button[data-control-name='continue_unify']",
                "button:contains('Submit')",
                "button:contains('Send')"
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if submit_button.is_enabled():
                        break
                except NoSuchElementException:
                    continue
            
            if submit_button:
                await self._human_click(submit_button)
                await self._random_delay(2, 4)
                
                # Wait for confirmation or next page
                try:
                    # Look for success indicators
                    success_indicators = [
                        "Application sent",
                        "Application submitted",
                        "Thank you for applying"
                    ]
                    
                    for indicator in success_indicators:
                        if indicator.lower() in self.driver.page_source.lower():
                            logger.info("Application submitted successfully")
                            return True
                    
                    # If no explicit success message, check if we're on a different page
                    await asyncio.sleep(2)
                    if self.driver.current_url != self.current_job_url:
                        logger.info("Application likely submitted (page changed)")
                        return True
                        
                except Exception:
                    pass
                
                logger.warning("Application submission status unclear")
                return True  # Assume success if no clear failure
            else:
                logger.error("No submit button found")
                return False
                
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return False
    
    async def _upload_resume(self, resume_path: str) -> bool:
        """Upload resume file"""
        try:
            resume_file = Path(resume_path)
            if not resume_file.exists():
                logger.error(f"Resume file not found: {resume_path}")
                return False
            
            # Look for file input
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['form']['file_input'])
            
            for file_input in file_inputs:
                try:
                    # Check if this is for resume/CV
                    parent_text = file_input.find_element(By.XPATH, "..").text.lower()
                    if any(keyword in parent_text for keyword in ['resume', 'cv', 'upload']):
                        file_input.send_keys(str(resume_file.absolute()))
                        await self._random_delay(1, 2)
                        logger.debug("Resume uploaded to file input")
                        return True
                except Exception:
                    continue
            
            # If no specific resume input found, try first file input
            if file_inputs:
                file_inputs[0].send_keys(str(resume_file.absolute()))
                await self._random_delay(1, 2)
                logger.debug("Resume uploaded to first file input")
                return True
            
            logger.warning("No file input found for resume upload")
            return False
            
        except Exception as e:
            logger.error(f"Error uploading resume: {e}")
            return False
    
    async def _fill_text_fields(self, cover_letter: str = None, custom_message: str = None):
        """Fill text areas and inputs"""
        try:
            # Fill text areas (usually for cover letters or messages)
            text_areas = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['form']['text_area'])
            
            for text_area in text_areas:
                try:
                    # Determine what type of input this is based on labels or placeholders
                    label_text = ""
                    try:
                        label = text_area.find_element(By.XPATH, ".//preceding::label[1]")
                        label_text = label.text.lower()
                    except:
                        label_text = text_area.get_attribute("placeholder", "").lower()
                    
                    # Fill with appropriate content
                    if "cover" in label_text or "letter" in label_text:
                        if cover_letter:
                            await self._human_type(text_area, cover_letter[:1000])  # Limit length
                    elif "message" in label_text or "note" in label_text:
                        message = custom_message or "I am very interested in this position and believe my skills would be a great fit for your team."
                        await self._human_type(text_area, message)
                    
                except Exception:
                    continue
            
        except Exception as e:
            logger.error(f"Error filling text fields: {e}")
    
    async def _handle_additional_fields(self):
        """Handle additional form fields like dropdowns, checkboxes, etc."""
        try:
            # Handle dropdowns/selects
            selects = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['form']['select'])
            for select in selects:
                try:
                    # Select first valid option (skip "Please select" type options)
                    options = select.find_elements(By.TAG_NAME, "option")
                    for option in options[1:]:  # Skip first option
                        if option.get_attribute("value"):
                            option.click()
                            break
                except Exception:
                    continue
            
            # Handle required checkboxes (like terms and conditions)
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['form']['checkbox'])
            for checkbox in checkboxes:
                try:
                    if not checkbox.is_selected():
                        # Check if it's a required checkbox
                        parent = checkbox.find_element(By.XPATH, "..")
                        if "required" in parent.get_attribute("class", "").lower():
                            await self._human_click(checkbox)
                except Exception:
                    continue
            
        except Exception as e:
            logger.error(f"Error handling additional fields: {e}")
    
    async def _human_click(self, element):
        """Simulate human-like clicking"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            await self._random_delay(0.1, 0.3)
            
            # Move to element and click
            webdriver.ActionChains(self.driver).move_to_element(element).click().perform()
            await self._random_delay(0.1, 0.5)
            
        except ElementClickInterceptedException:
            # Try JavaScript click if regular click fails
            self.driver.execute_script("arguments[0].click();", element)
            await self._random_delay(0.1, 0.3)
    
    async def _human_type(self, element, text: str):
        """Simulate human-like typing"""
        try:
            element.clear()
            await self._random_delay(0.1, 0.3)
            
            # Type with random delays between characters
            for char in text:
                element.send_keys(char)
                if random.random() < 0.1:  # Random pause 10% of the time
                    await self._random_delay(0.05, 0.2)
            
        except Exception as e:
            # Fallback to regular send_keys
            element.clear()
            element.send_keys(text)
    
    async def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Add random delay to simulate human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def close(self):
        """Close the browser and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logged_in = False
                logger.info("LinkedIn bot closed successfully")
        except Exception as e:
            logger.error(f"Error closing LinkedIn bot: {e}")
    
    def __del__(self):
        """Cleanup on object destruction"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass