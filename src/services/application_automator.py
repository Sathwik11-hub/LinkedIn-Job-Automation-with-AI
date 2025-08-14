"""LinkedIn application automation service."""

import time
import random
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..core import LoggerMixin, get_settings
from ..models import JobPosting, CoverLetter, ApplicationRecord, ApplicationStatus
from .linkedin_scraper import LinkedInScraper


class ApplicationAutomator(LoggerMixin):
    """Automate job applications on LinkedIn."""
    
    def __init__(self):
        self.settings = get_settings()
        self.scraper = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.scraper = LinkedInScraper()
        await self.scraper.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.scraper:
            await self.scraper.__aexit__(exc_type, exc_val, exc_tb)
    
    def apply_to_jobs(
        self, 
        job_postings: List[JobPosting],
        cover_letters: Dict[str, CoverLetter],
        dry_run: bool = True
    ) -> List[ApplicationRecord]:
        """Apply to multiple jobs with cover letters."""
        if not self.scraper.is_logged_in:
            if not self.scraper.login():
                raise Exception("Failed to login to LinkedIn")
        
        application_records = []
        applications_today = 0
        max_applications = self.settings.max_applications_per_day
        
        self.logger.info(f"Starting application process for {len(job_postings)} jobs (dry_run={dry_run})")
        
        for job in job_postings:
            if applications_today >= max_applications:
                self.logger.info(f"Reached daily application limit of {max_applications}")
                break
            
            try:
                # Get cover letter for this job
                cover_letter = cover_letters.get(job.job_id)
                
                # Apply to job
                record = self._apply_to_single_job(job, cover_letter, dry_run)
                application_records.append(record)
                
                if record.status == ApplicationStatus.APPLIED:
                    applications_today += 1
                
                # Add delay between applications
                if not dry_run:
                    delay = self.settings.application_delay_seconds + random.randint(5, 15)
                    self.logger.info(f"Waiting {delay} seconds before next application")
                    time.sleep(delay)
                
            except Exception as e:
                self.logger.error(f"Failed to apply to job {job.job_id}: {str(e)}")
                error_record = ApplicationRecord(
                    job_id=job.job_id,
                    job_title=job.title,
                    company=job.company,
                    status=ApplicationStatus.ERROR,
                    error_message=str(e)
                )
                application_records.append(error_record)
        
        self.logger.info(f"Application process completed. Applied to {applications_today} jobs")
        return application_records
    
    def _apply_to_single_job(
        self, 
        job: JobPosting, 
        cover_letter: Optional[CoverLetter] = None,
        dry_run: bool = True
    ) -> ApplicationRecord:
        """Apply to a single job."""
        self.logger.info(f"{'[DRY RUN] ' if dry_run else ''}Applying to: {job.title} at {job.company}")
        
        try:
            # Navigate to job page
            self.scraper.driver.get(job.url)
            time.sleep(3)
            
            # Check if Easy Apply is available
            if not self._has_easy_apply():
                return ApplicationRecord(
                    job_id=job.job_id,
                    job_title=job.title,
                    company=job.company,
                    status=ApplicationStatus.SKIPPED,
                    notes="Easy Apply not available"
                )
            
            if dry_run:
                return ApplicationRecord(
                    job_id=job.job_id,
                    job_title=job.title,
                    company=job.company,
                    status=ApplicationStatus.PENDING,
                    notes="Dry run - would apply with Easy Apply"
                )
            
            # Click Easy Apply button
            easy_apply_btn = WebDriverWait(self.scraper.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            easy_apply_btn.click()
            time.sleep(2)
            
            # Fill application form
            success = self._fill_application_form(cover_letter)
            
            if success:
                return ApplicationRecord(
                    job_id=job.job_id,
                    job_title=job.title,
                    company=job.company,
                    status=ApplicationStatus.APPLIED,
                    cover_letter_id=cover_letter.job_id if cover_letter else None,
                    notes="Successfully applied via Easy Apply"
                )
            else:
                return ApplicationRecord(
                    job_id=job.job_id,
                    job_title=job.title,
                    company=job.company,
                    status=ApplicationStatus.ERROR,
                    error_message="Failed to complete application form"
                )
                
        except Exception as e:
            self.logger.error(f"Error applying to job: {str(e)}")
            return ApplicationRecord(
                job_id=job.job_id,
                job_title=job.title,
                company=job.company,
                status=ApplicationStatus.ERROR,
                error_message=str(e)
            )
    
    def _has_easy_apply(self) -> bool:
        """Check if the job has Easy Apply option."""
        try:
            easy_apply_buttons = self.scraper.driver.find_elements(
                By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"
            )
            return len(easy_apply_buttons) > 0
        except:
            return False
    
    def _fill_application_form(self, cover_letter: Optional[CoverLetter] = None) -> bool:
        """Fill out the Easy Apply application form."""
        try:
            # Wait for the modal to appear
            WebDriverWait(self.scraper.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-easy-apply-modal"))
            )
            
            step = 1
            max_steps = 5
            
            while step <= max_steps:
                self.logger.info(f"Processing application step {step}")
                
                # Check for common form fields and fill them
                self._fill_contact_info()
                self._fill_experience_questions()
                
                # Add cover letter if available and field exists
                if cover_letter:
                    self._add_cover_letter(cover_letter.content)
                
                # Look for next button or submit button
                next_btn = self._find_next_or_submit_button()
                
                if not next_btn:
                    self.logger.warning("No next/submit button found")
                    return False
                
                button_text = next_btn.text.lower()
                
                # If it's a submit button, complete the application
                if any(word in button_text for word in ['submit', 'send application', 'apply']):
                    self.logger.info("Submitting application")
                    next_btn.click()
                    time.sleep(3)
                    
                    # Check for confirmation
                    if self._check_application_confirmation():
                        self.logger.info("Application submitted successfully")
                        return True
                    else:
                        self.logger.warning("Application submission may have failed")
                        return False
                
                # If it's a next button, continue to next step
                elif 'next' in button_text or 'continue' in button_text:
                    next_btn.click()
                    time.sleep(2)
                    step += 1
                else:
                    self.logger.warning(f"Unexpected button text: {button_text}")
                    return False
            
            self.logger.warning("Reached maximum steps without completing application")
            return False
            
        except TimeoutException:
            self.logger.error("Timeout while filling application form")
            return False
        except Exception as e:
            self.logger.error(f"Error filling application form: {str(e)}")
            return False
    
    def _fill_contact_info(self):
        """Fill contact information fields."""
        try:
            # Phone number
            phone_fields = self.scraper.driver.find_elements(
                By.XPATH, "//input[contains(@id, 'phone') or contains(@name, 'phone')]"
            )
            for field in phone_fields:
                if not field.get_attribute('value'):
                    field.clear()
                    field.send_keys("(555) 123-4567")  # Placeholder phone
            
            # Email is usually pre-filled
            
        except Exception as e:
            self.logger.debug(f"Error filling contact info: {str(e)}")
    
    def _fill_experience_questions(self):
        """Fill experience-related questions."""
        try:
            # Look for dropdown questions
            dropdowns = self.scraper.driver.find_elements(By.TAG_NAME, "select")
            for dropdown in dropdowns:
                # Common experience questions
                if any(keyword in dropdown.get_attribute('id').lower() for keyword in ['experience', 'years']):
                    # Select a reasonable option (usually 2-5 years)
                    options = dropdown.find_elements(By.TAG_NAME, "option")
                    if len(options) > 2:
                        options[2].click()  # Select third option
            
            # Look for yes/no questions
            checkboxes = self.scraper.driver.find_elements(
                By.XPATH, "//input[@type='radio' or @type='checkbox']"
            )
            for checkbox in checkboxes:
                parent_text = checkbox.find_element(By.XPATH, "..").text.lower()
                
                # Answer yes to work authorization questions
                if any(keyword in parent_text for keyword in ['authorized', 'eligible', 'visa', 'citizen']):
                    if 'yes' in parent_text:
                        checkbox.click()
                
                # Answer yes to experience questions if reasonable
                if any(keyword in parent_text for keyword in ['experience', 'familiar']):
                    if 'yes' in parent_text:
                        checkbox.click()
                        
        except Exception as e:
            self.logger.debug(f"Error filling experience questions: {str(e)}")
    
    def _add_cover_letter(self, cover_letter_content: str):
        """Add cover letter to application."""
        try:
            # Look for cover letter text area
            text_areas = self.scraper.driver.find_elements(By.TAG_NAME, "textarea")
            
            for text_area in text_areas:
                # Check if it's a cover letter field
                field_id = text_area.get_attribute('id').lower()
                field_name = text_area.get_attribute('name').lower()
                
                if any(keyword in field_id + field_name for keyword in ['cover', 'letter', 'message', 'note']):
                    text_area.clear()
                    text_area.send_keys(cover_letter_content)
                    self.logger.info("Cover letter added to application")
                    break
                    
        except Exception as e:
            self.logger.debug(f"Error adding cover letter: {str(e)}")
    
    def _find_next_or_submit_button(self):
        """Find the next or submit button in the application form."""
        try:
            # Look for buttons with common text
            buttons = self.scraper.driver.find_elements(By.TAG_NAME, "button")
            
            for button in buttons:
                button_text = button.text.lower()
                if any(word in button_text for word in [
                    'next', 'continue', 'submit', 'send application', 'apply', 'review'
                ]):
                    if button.is_enabled() and button.is_displayed():
                        return button
            
            # Fallback: look for buttons with specific aria-labels
            submit_buttons = self.scraper.driver.find_elements(
                By.XPATH, "//button[contains(@aria-label, 'Submit') or contains(@aria-label, 'Continue')]"
            )
            
            for button in submit_buttons:
                if button.is_enabled() and button.is_displayed():
                    return button
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error finding next/submit button: {str(e)}")
            return None
    
    def _check_application_confirmation(self) -> bool:
        """Check if application was submitted successfully."""
        try:
            # Wait for confirmation message or redirect
            time.sleep(3)
            
            # Look for success messages
            success_indicators = [
                "application sent",
                "application submitted",
                "thank you for applying",
                "we have received your application"
            ]
            
            page_text = self.scraper.driver.page_source.lower()
            
            for indicator in success_indicators:
                if indicator in page_text:
                    return True
            
            # Check if we're redirected away from the application modal
            try:
                self.scraper.driver.find_element(By.CSS_SELECTOR, ".jobs-easy-apply-modal")
                return False  # Modal still present, likely not submitted
            except NoSuchElementException:
                return True  # Modal gone, likely submitted
                
        except Exception as e:
            self.logger.debug(f"Error checking confirmation: {str(e)}")
            return False
    
    def withdraw_application(self, job_url: str) -> bool:
        """Withdraw an application (if supported by LinkedIn)."""
        try:
            self.scraper.driver.get(job_url)
            time.sleep(3)
            
            # Look for withdraw button
            withdraw_buttons = self.scraper.driver.find_elements(
                By.XPATH, "//button[contains(text(), 'Withdraw')]"
            )
            
            if withdraw_buttons:
                withdraw_buttons[0].click()
                time.sleep(2)
                
                # Confirm withdrawal
                confirm_buttons = self.scraper.driver.find_elements(
                    By.XPATH, "//button[contains(text(), 'Confirm') or contains(text(), 'Yes')]"
                )
                
                if confirm_buttons:
                    confirm_buttons[0].click()
                    self.logger.info("Application withdrawn successfully")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error withdrawing application: {str(e)}")
            return False