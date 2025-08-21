"""
Automated job application service
Orchestrates the entire application process
"""

import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

from app.models.job_schema import Job, ApplicationTracker, ApplicationStatus
from app.services.job_scraper import JobScraper
from app.services.matcher import JobMatcher
from app.services.cover_letter_generator import CoverLetterGenerator
from automation.linkedin_bot import LinkedInBot
from app.config import settings
from app.utils.logger import setup_logger, log_async_performance, StructuredLogger

logger = setup_logger(__name__)
structured_logger = StructuredLogger(__name__)


class AutoApply:
    """
    Automated job application orchestrator
    """
    
    def __init__(self):
        self.job_scraper = JobScraper()
        self.job_matcher = JobMatcher()
        self.cover_letter_generator = CoverLetterGenerator()
        self.linkedin_bot = LinkedInBot()
        
        # Application tracking
        self.applications = []
        self.daily_application_count = 0
        self.last_reset_date = datetime.utcnow().date()
        
        # Application state
        self.is_running = False
        self.current_session = None
    
    @log_async_performance
    async def apply_to_job(
        self,
        job_id: str,
        resume_path: str,
        cover_letter_template: Optional[str] = None,
        custom_message: Optional[str] = None
    ) -> ApplicationTracker:
        """
        Apply to a single job
        
        Args:
            job_id: LinkedIn job ID
            resume_path: Path to resume file
            cover_letter_template: Cover letter template to use
            custom_message: Custom message for application
            
        Returns:
            Application tracking information
        """
        application_id = f"app_{job_id}_{int(datetime.utcnow().timestamp())}"
        
        try:
            # Check daily limit
            self._check_daily_limit()
            
            # Get job details
            job = await self.job_scraper.get_job_details(job_id)
            if not job:
                raise ValueError(f"Could not retrieve job details for {job_id}")
            
            logger.info(f"Starting application to {job.title} at {job.company}")
            
            # Generate cover letter
            cover_letter = await self.cover_letter_generator.generate_cover_letter(
                job, resume_path, cover_letter_template
            )
            
            # Initialize application tracker
            tracker = ApplicationTracker(
                id=application_id,
                job_id=job_id,
                job_title=job.title,
                company=job.company,
                status=ApplicationStatus.PENDING,
                applied_date=datetime.utcnow(),
                resume_used=resume_path,
                cover_letter_id=cover_letter.job_id,
                custom_message=custom_message,
                auto_applied=True
            )
            
            # Perform automated application
            success = await self._perform_application(job, resume_path, cover_letter.content, custom_message)
            
            if success:
                tracker.status = ApplicationStatus.APPLIED
                self.daily_application_count += 1
                structured_logger.log_job_application(job_id, job.company, job.title, True)
                logger.info(f"Successfully applied to {job.title} at {job.company}")
            else:
                tracker.status = ApplicationStatus.PENDING
                tracker.automation_errors.append("Application submission failed")
                structured_logger.log_job_application(job_id, job.company, job.title, False)
                logger.warning(f"Failed to apply to {job.title} at {job.company}")
            
            # Track application
            self.applications.append(tracker)
            
            return tracker
            
        except Exception as e:
            logger.error(f"Error applying to job {job_id}: {e}")
            
            # Create error tracker
            tracker = ApplicationTracker(
                id=application_id,
                job_id=job_id,
                job_title="Unknown",
                company="Unknown",
                status=ApplicationStatus.PENDING,
                applied_date=datetime.utcnow(),
                resume_used=resume_path,
                automation_errors=[str(e)],
                auto_applied=True
            )
            
            self.applications.append(tracker)
            return tracker
    
    @log_async_performance
    async def bulk_apply(
        self,
        job_ids: List[str],
        resume_path: str,
        delay_between_applications: float = None
    ) -> List[ApplicationTracker]:
        """
        Apply to multiple jobs in bulk
        
        Args:
            job_ids: List of LinkedIn job IDs
            resume_path: Path to resume file
            delay_between_applications: Delay between applications (seconds)
            
        Returns:
            List of application tracking information
        """
        delay = delay_between_applications or settings.automation_delay
        results = []
        
        logger.info(f"Starting bulk application to {len(job_ids)} jobs")
        
        for i, job_id in enumerate(job_ids):
            try:
                # Check if we've hit daily limit
                if self.daily_application_count >= settings.max_applications_per_day:
                    logger.warning(f"Daily application limit reached ({settings.max_applications_per_day})")
                    break
                
                # Apply to job
                tracker = await self.apply_to_job(job_id, resume_path)
                results.append(tracker)
                
                # Log progress
                logger.info(f"Bulk apply progress: {i+1}/{len(job_ids)} completed")
                
                # Delay between applications to avoid rate limiting
                if i < len(job_ids) - 1:  # Don't delay after the last application
                    await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Error in bulk apply for job {job_id}: {e}")
                continue
        
        logger.info(f"Bulk application completed: {len(results)} applications processed")
        return results
    
    @log_async_performance
    async def smart_apply(
        self,
        search_criteria: Dict[str, Any],
        resume_path: str,
        max_applications: int = 10,
        min_match_score: float = 0.6
    ) -> List[ApplicationTracker]:
        """
        Intelligently search and apply to matching jobs
        
        Args:
            search_criteria: Job search parameters
            resume_path: Path to resume file
            max_applications: Maximum number of applications to submit
            min_match_score: Minimum match score threshold
            
        Returns:
            List of application tracking information
        """
        try:
            logger.info(f"Starting smart apply with criteria: {search_criteria}")
            
            # Search for jobs
            jobs = await self.job_scraper.search_jobs(
                keywords=search_criteria.get('keywords', ''),
                location=search_criteria.get('location', 'United States'),
                job_type=search_criteria.get('job_type'),
                experience_level=search_criteria.get('experience_level'),
                limit=max_applications * 3  # Get more jobs to filter from
            )
            
            logger.info(f"Found {len(jobs)} jobs for matching")
            
            # Match and rank jobs
            matched_jobs = await self.job_matcher.match_jobs(jobs, resume_path, top_k=max_applications * 2)
            
            # Filter by minimum match score
            qualified_jobs = [
                job for job in matched_jobs 
                if job.match_score and job.match_score >= min_match_score
            ]
            
            logger.info(f"Found {len(qualified_jobs)} jobs meeting minimum match score of {min_match_score}")
            
            # Apply to top matching jobs
            top_jobs = qualified_jobs[:max_applications]
            job_ids = [job.id for job in top_jobs]
            
            results = await self.bulk_apply(job_ids, resume_path)
            
            # Log insights
            if top_jobs:
                avg_match_score = sum(job.match_score for job in top_jobs) / len(top_jobs)
                logger.info(f"Smart apply completed with average match score: {avg_match_score:.2f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in smart apply: {e}")
            return []
    
    async def _perform_application(
        self,
        job: Job,
        resume_path: str,
        cover_letter: str,
        custom_message: Optional[str] = None
    ) -> bool:
        """
        Perform the actual application using LinkedIn bot
        
        Args:
            job: Job information
            resume_path: Path to resume file
            cover_letter: Generated cover letter content
            custom_message: Custom message for application
            
        Returns:
            True if application was successful, False otherwise
        """
        try:
            # Start LinkedIn bot session if not already started
            if not self.linkedin_bot.is_logged_in():
                await self.linkedin_bot.login()
            
            # Navigate to job page
            await self.linkedin_bot.navigate_to_job(job.linkedin_url)
            
            # Check if job is still available and we can apply
            if not await self.linkedin_bot.can_apply_to_job():
                logger.warning(f"Cannot apply to job {job.id} - may already be applied or not available")
                return False
            
            # Click apply button
            await self.linkedin_bot.click_apply_button()
            
            # Fill application form
            success = await self.linkedin_bot.fill_application_form(
                resume_path=resume_path,
                cover_letter=cover_letter,
                custom_message=custom_message
            )
            
            if success:
                # Submit application
                await self.linkedin_bot.submit_application()
                
                # Add delay to avoid detection
                await asyncio.sleep(settings.automation_delay)
                
                return True
            else:
                logger.warning(f"Failed to fill application form for job {job.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error performing application for job {job.id}: {e}")
            return False
    
    def _check_daily_limit(self):
        """Check and reset daily application limit"""
        current_date = datetime.utcnow().date()
        
        # Reset counter if it's a new day
        if current_date != self.last_reset_date:
            self.daily_application_count = 0
            self.last_reset_date = current_date
            logger.info("Daily application count reset")
        
        # Check if limit exceeded
        if self.daily_application_count >= settings.max_applications_per_day:
            raise Exception(f"Daily application limit reached ({settings.max_applications_per_day})")
    
    async def get_application_status(self) -> Dict[str, Any]:
        """Get current application status and statistics"""
        
        total_applications = len(self.applications)
        successful_applications = len([app for app in self.applications if app.status == ApplicationStatus.APPLIED])
        pending_applications = len([app for app in self.applications if app.status == ApplicationStatus.PENDING])
        
        # Recent activity (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_applications = [
            app for app in self.applications 
            if app.applied_date >= yesterday
        ]
        
        return {
            'total_applications': total_applications,
            'successful_applications': successful_applications,
            'pending_applications': pending_applications,
            'daily_count': self.daily_application_count,
            'daily_limit': settings.max_applications_per_day,
            'recent_activity': len(recent_applications),
            'is_running': self.is_running,
            'last_application': self.applications[-1].applied_date.isoformat() if self.applications else None,
            'success_rate': (successful_applications / total_applications * 100) if total_applications > 0 else 0
        }
    
    async def get_application_history(
        self,
        limit: int = 50,
        status_filter: Optional[ApplicationStatus] = None
    ) -> List[ApplicationTracker]:
        """Get application history with optional filtering"""
        
        applications = self.applications
        
        # Filter by status if specified
        if status_filter:
            applications = [app for app in applications if app.status == status_filter]
        
        # Sort by application date (most recent first)
        applications.sort(key=lambda x: x.applied_date, reverse=True)
        
        # Limit results
        return applications[:limit]
    
    async def retry_failed_applications(self, resume_path: str) -> List[ApplicationTracker]:
        """Retry applications that failed"""
        
        failed_applications = [
            app for app in self.applications 
            if app.status == ApplicationStatus.PENDING and app.automation_errors
        ]
        
        logger.info(f"Retrying {len(failed_applications)} failed applications")
        
        results = []
        for app in failed_applications:
            try:
                # Retry the application
                new_tracker = await self.apply_to_job(app.job_id, resume_path)
                results.append(new_tracker)
                
                # Remove old failed tracker
                self.applications.remove(app)
                
            except Exception as e:
                logger.error(f"Error retrying application {app.id}: {e}")
                continue
        
        return results
    
    async def start_continuous_apply(
        self,
        search_criteria: Dict[str, Any],
        resume_path: str,
        check_interval: int = 3600  # 1 hour
    ):
        """Start continuous job application process"""
        
        self.is_running = True
        logger.info("Starting continuous application process")
        
        try:
            while self.is_running:
                try:
                    # Check if we can still apply today
                    if self.daily_application_count >= settings.max_applications_per_day:
                        logger.info("Daily limit reached, waiting for next day")
                        await asyncio.sleep(check_interval)
                        continue
                    
                    # Perform smart apply
                    remaining_applications = settings.max_applications_per_day - self.daily_application_count
                    
                    await self.smart_apply(
                        search_criteria=search_criteria,
                        resume_path=resume_path,
                        max_applications=min(remaining_applications, 5)  # Apply to max 5 at a time
                    )
                    
                    # Wait before next iteration
                    logger.info(f"Waiting {check_interval} seconds before next application cycle")
                    await asyncio.sleep(check_interval)
                    
                except Exception as e:
                    logger.error(f"Error in continuous apply cycle: {e}")
                    await asyncio.sleep(60)  # Wait 1 minute before retrying
                    
        except asyncio.CancelledError:
            logger.info("Continuous application process cancelled")
        finally:
            self.is_running = False
    
    def stop_continuous_apply(self):
        """Stop continuous application process"""
        self.is_running = False
        logger.info("Stopping continuous application process")
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            self.job_scraper.close()
            await self.linkedin_bot.close()
            logger.info("AutoApply cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")