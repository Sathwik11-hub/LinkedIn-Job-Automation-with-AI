"""
AutoAgentHire - Complete LinkedIn Job Automation Bot
Handles browser automation, job search, AI analysis, and auto-apply
"""

import asyncio
import random
import re
import time
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()


class AutoAgentHireBot:
    """Complete LinkedIn automation with AI-powered job matching and auto-apply"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.resume_text = ""
        self.jobs_data = []
        self.applied_jobs = []
        self.errors = []
        
        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and not api_key.startswith('your_'):
            genai.configure(api_key=api_key)
            self.ai_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.ai_model = None
    
    async def initialize_browser(self) -> None:
        """Initialize Playwright browser with anti-detection"""
        playwright = await async_playwright().start()
        
        self.browser = await playwright.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            geolocation={'longitude': -74.0060, 'latitude': 40.7128},
            permissions=['geolocation']
        )
        
        # Anti-detection scripts
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)
        
        self.page = await self.context.new_page()
        print("✅ Browser initialized with anti-detection")
    
    async def login_linkedin(self) -> bool:
        """Login to LinkedIn with credentials from .env"""
        try:
            email = os.getenv('LINKEDIN_EMAIL')
            password = os.getenv('LINKEDIN_PASSWORD')
            
            if not email or not password:
                raise Exception("LinkedIn credentials not found in .env file")
            
            print("🔐 Navigating to LinkedIn login...")
            # Try with longer timeout and load instead of networkidle
            try:
                await self.page.goto('https://www.linkedin.com/login', wait_until='load', timeout=60000)
            except:
                # Fallback: try domcontentloaded
                print("⚠️  Network slow, using fallback loading...")
                await self.page.goto('https://www.linkedin.com/login', wait_until='domcontentloaded', timeout=60000)
            
            await asyncio.sleep(random.uniform(2, 3))
            
            # Fill email
            print("📧 Entering email...")
            await self.page.fill('input[name="session_key"]', email)
            await asyncio.sleep(random.uniform(1.5, 2.5))
            
            # Fill password
            print("🔑 Entering password...")
            await self.page.fill('input[name="session_password"]', password)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Click sign in
            print("👆 Clicking Sign In...")
            await self.page.click('button[type="submit"]')
            await asyncio.sleep(5)
            
            # Check for 2FA or verification
            current_url = self.page.url
            if 'checkpoint' in current_url or 'challenge' in current_url:
                print("⚠️  Security challenge detected. Please complete manually...")
                print("⏳ Waiting 60 seconds for manual verification...")
                await asyncio.sleep(60)
            
            # Verify login success
            if 'feed' in self.page.url or 'mynetwork' in self.page.url:
                print("✅ Successfully logged into LinkedIn!")
                return True
            else:
                print(f"❌ Login may have failed. Current URL: {self.page.url}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {str(e)}")
            self.errors.append(f"Login failed: {str(e)}")
            return False
    
    async def search_jobs(self, keyword: str, location: str) -> None:
        """Search for jobs with Easy Apply filter"""
        try:
            print(f"🔍 Searching for '{keyword}' jobs in '{location}'...")

            # Navigate to jobs section with better timeout and error handling
            try:
                await self.page.goto('https://www.linkedin.com/jobs/', wait_until='load', timeout=60000)
            except Exception as nav_error:
                print(f"⚠️  Navigation failed: {str(nav_error)}")
                try:
                    await self.page.goto('https://www.linkedin.com/jobs/', wait_until='domcontentloaded', timeout=60000)
                except Exception as fallback_error:
                    print(f"⚠️  Fallback navigation also failed: {str(fallback_error)}")
                    raise Exception(f"Could not navigate to jobs page: {str(nav_error)}")

            await asyncio.sleep(random.uniform(2, 3))

            # Try different selectors for keyword input with shorter timeouts
            print("📝 Entering job keyword...")
            keyword_input = None
            selectors = [
                'input[aria-label*="Search by title"]',
                'input[aria-label*="Search job titles"]',
                'input.jobs-search-box__text-input',
                'input[placeholder*="Search job titles"]',
                '#jobs-search-box-keyword-id-ember',
                'input[id*="jobs-search-box-keyword"]'
            ]

            for selector in selectors:
                try:
                    keyword_input = await self.page.wait_for_selector(selector, timeout=3000)
                    if keyword_input:
                        print(f"✅ Found keyword input with selector: {selector}")
                        break
                except:
                    continue

            if not keyword_input:
                print("⚠️  Could not find keyword input, trying direct URL...")
                # Use direct URL with search parameters
                search_url = f'https://www.linkedin.com/jobs/search/?keywords={keyword.replace(" ", "%20")}&location={location.replace(" ", "%20")}&f_AL=true'
                try:
                    await self.page.goto(search_url, wait_until='load', timeout=60000)
                    await asyncio.sleep(random.uniform(2, 3))
                    print("✅ Navigated to search results via URL")
                    return
                except Exception as url_error:
                    raise Exception(f"Direct URL navigation failed: {str(url_error)}")

            await keyword_input.fill(keyword)
            await asyncio.sleep(random.uniform(1, 2))

            # Try to find and fill location input
            location_selectors = [
                'input[aria-label*="City"]',
                'input[aria-label*="Location"]',
                'input[placeholder*="Location"]',
                'input[id*="jobs-search-box-location"]'
            ]

            for selector in location_selectors:
                try:
                    location_input = await self.page.wait_for_selector(selector, timeout=2000)
                    if location_input:
                        await location_input.fill(location)
                        print("✅ Location filled")
                        break
                except:
                    continue

            # Press Enter to search
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(random.uniform(2, 4))

            print("✅ Job search completed")

        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")
            await keyword_input.fill(keyword)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Enter location
            print("📍 Entering location...")
            location_input = await self.page.wait_for_selector('input[aria-label*="City"]', timeout=10000)
            await location_input.fill(location)
            await asyncio.sleep(random.uniform(1, 2))
            
            # Search
            print("🚀 Executing search...")
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(5)
            
            # Apply Easy Apply filter
            print("✨ Applying Easy Apply filter...")
            try:
                # Look for Easy Apply filter button
                easy_apply_button = await self.page.wait_for_selector(
                    'button:has-text("Easy Apply")', 
                    timeout=5000
                )
                await easy_apply_button.click()
                await asyncio.sleep(3)
                print("✅ Easy Apply filter activated")
            except:
                print("⚠️  Easy Apply filter not found, continuing with all jobs...")
            
            # Apply experience level filter if specified
            experience = self.config.get('experience_level', 'Any')
            if experience != 'Any':
                try:
                    await self._apply_filter('Experience level', experience)
                except:
                    print(f"⚠️  Could not apply experience filter: {experience}")
            
            # Apply job type filter if specified
            job_type = self.config.get('job_type', 'Any')
            if job_type != 'Any':
                try:
                    await self._apply_filter('Job type', job_type)
                except:
                    print(f"⚠️  Could not apply job type filter: {job_type}")
            
            await asyncio.sleep(3)
            print("✅ Search filters applied successfully")
            
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            self.errors.append(f"Search failed: {str(e)}")
    
    async def _apply_filter(self, filter_name: str, value: str) -> None:
        """Helper to apply a specific filter"""
        try:
            # Click filter button
            filter_button = await self.page.wait_for_selector(
                f'button:has-text("{filter_name}")',
                timeout=5000
            )
            await filter_button.click()
            await asyncio.sleep(1)
            
            # Select option
            option = await self.page.wait_for_selector(
                f'label:has-text("{value}")',
                timeout=5000
            )
            await option.click()
            await asyncio.sleep(1)
            
            # Apply
            apply_button = await self.page.wait_for_selector(
                'button:has-text("Apply")',
                timeout=5000
            )
            await apply_button.click()
            await asyncio.sleep(2)
            
        except Exception as e:
            raise Exception(f"Failed to apply {filter_name} filter: {str(e)}")
    
    async def collect_job_listings(self, max_jobs: int = 30) -> List[Dict]:
        """Scroll and collect job listings"""
        jobs = []
        
        try:
            print(f"📊 Collecting up to {max_jobs} job listings...")
            
            # Scroll to load more jobs
            for scroll in range(5):
                await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(2)
            
            # Get job cards
            job_cards = await self.page.query_selector_all('div.job-card-container')
            
            if not job_cards:
                # Try alternative selector
                job_cards = await self.page.query_selector_all('li.jobs-search-results__list-item')
            
            print(f"🔢 Found {len(job_cards)} job cards")
            
            for i, card in enumerate(job_cards[:max_jobs]):
                try:
                    # Check if we should continue (handle interruptions)
                    if len(jobs) >= max_jobs:
                        break

                    # Click to select job with error handling
                    try:
                        await card.click()
                        await asyncio.sleep(random.uniform(1, 2))
                    except Exception as click_error:
                        print(f"⚠️  Could not click job card {i+1}: {str(click_error)}")
                        continue

                    # Extract job details with multiple selector fallbacks
                    title = None
                    company = None
                    location = None

                    # Try multiple selectors for job title
                    title_selectors = [
                        'h1.job-details-jobs-unified-top-card__job-title',
                        'h1[data-test-id="job-title"]',
                        'h1.t-24',
                        'h1.job-title',
                        'h1'
                    ]

                    for selector in title_selectors:
                        try:
                            title = await self.page.text_content(selector, timeout=5000)
                            if title and title.strip():
                                break
                        except:
                            continue

                    # Try multiple selectors for company
                    company_selectors = [
                        'a.job-details-jobs-unified-top-card__company-name',
                        'a[data-test-id="company-name"]',
                        'a.job-company',
                        'span.company-name',
                        'a[href*="/company/"]'
                    ]

                    for selector in company_selectors:
                        try:
                            company = await self.page.text_content(selector, timeout=5000)
                            if company and company.strip():
                                break
                        except:
                            continue

                    # Try multiple selectors for location
                    location_selectors = [
                        'span.job-details-jobs-unified-top-card__bullet',
                        'span[data-test-id="job-location"]',
                        'span.job-location',
                        'span.location'
                    ]

                    for selector in location_selectors:
                        try:
                            location = await self.page.text_content(selector, timeout=5000)
                            if location and location.strip():
                                break
                        except:
                            continue

                    # Get job URL
                    url = self.page.url

                    # Check for Easy Apply badge with multiple selectors
                    easy_apply = False
                    easy_apply_selectors = [
                        'button.jobs-apply-button',
                        'button[aria-label*="Easy Apply"]',
                        'button[data-test-id="easy-apply-button"]',
                        'button.jobs-easy-apply-button'
                    ]

                    for selector in easy_apply_selectors:
                        try:
                            await self.page.wait_for_selector(selector, timeout=2000)
                            easy_apply = True
                            break
                        except:
                            continue

                    if title and title.strip():
                        job_data = {
                            'title': title.strip(),
                            'company': company.strip() if company else 'Unknown Company',
                            'location': location.strip() if location else 'Unknown Location',
                            'url': url,
                            'easy_apply': easy_apply,
                            'index': i + 1
                        }
                        jobs.append(job_data)
                        print(f"✅ Job {len(jobs)}: {title.strip()[:50]}... at {company.strip()[:30] if company else 'Unknown'}...")

                except Exception as e:
                    print(f"⚠️  Error extracting job {i+1}: {str(e)}")
                    continue                    # Get job description
                    description = ""
                    try:
                        desc_element = await self.page.query_selector('div.jobs-description-content__text')
                        if desc_element:
                            description = await desc_element.text_content()
                    except:
                        description = "Description not available"
                    
                    job = {
                        'title': title.strip() if title else "Unknown",
                        'company': company.strip() if company else "Unknown",
                        'location': location.strip() if location else "Unknown",
                        'url': url,
                        'easy_apply': easy_apply,
                        'description': description.strip()[:1000]  # Limit description length
                    }
                    
                    jobs.append(job)
                    print(f"✅ Collected: {job['title']} at {job['company']}")
                    
                    if len(jobs) >= max_jobs:
                        break
                        
                except Exception as e:
                    print(f"⚠️  Error collecting job {i+1}: {str(e)}")
                    continue
            
            self.jobs_data = jobs
            print(f"📋 Total jobs collected: {len(jobs)}")
            return jobs
            
        except Exception as e:
            print(f"❌ Collection error: {str(e)}")
            self.errors.append(f"Job collection failed: {str(e)}")
            return jobs
    
    async def analyze_job_with_ai(self, job: Dict) -> Dict:
        """Analyze job compatibility using Gemini AI"""
        if not self.ai_model:
            # Fallback: simple keyword matching
            return self._simple_job_match(job)
        
        try:
            prompt = f"""
Analyze job compatibility and return ONLY valid JSON (no markdown, no code blocks):

RESUME:
{self.resume_text[:3000]}

JOB:
Title: {job['title']}
Company: {job['company']}
Description: {job['description']}

Return this exact JSON structure:
{{
    "similarity_score": <number 0-100>,
    "matching_skills": ["skill1", "skill2", "skill3"],
    "missing_skills": ["skill1", "skill2"],
    "recommendation": "APPLY or SKIP",
    "confidence": <number 0.0-1.0>,
    "reasoning": "brief explanation"
}}
"""
            
            response = await asyncio.to_thread(
                self.ai_model.generate_content,
                prompt
            )
            
            # Parse JSON from response
            result_text = response.text.strip()
            # Remove markdown code blocks if present
            result_text = re.sub(r'```json\n?', '', result_text)
            result_text = re.sub(r'```\n?', '', result_text)
            
            result = json.loads(result_text)
            
            print(f"🤖 AI Analysis: {result['recommendation']} (Score: {result['similarity_score']}%)")
            return result
            
        except Exception as e:
            print(f"⚠️  AI analysis error: {str(e)}, using fallback")
            return self._simple_job_match(job)
    
    def _simple_job_match(self, job: Dict) -> Dict:
        """Fallback: Simple keyword-based matching"""
        skills = self.config.get('skills', '').lower().split(',')
        job_text = f"{job['title']} {job['description']}".lower()
        
        matching_skills = [s.strip() for s in skills if s.strip() in job_text]
        score = min(len(matching_skills) * 20, 100)
        
        return {
            'similarity_score': score,
            'matching_skills': matching_skills[:5],
            'missing_skills': [],
            'recommendation': 'APPLY' if score >= 60 else 'SKIP',
            'confidence': 0.7,
            'reasoning': f"Matched {len(matching_skills)} skills from resume"
        }
    
    async def select_top_jobs(self, max_apply: int = 5) -> List[Dict]:
        """Select top jobs to apply based on AI analysis"""
        print(f"🎯 Analyzing jobs with AI to select top {max_apply}...")
        
        analyzed_jobs = []
        threshold = float(self.config.get('similarity_threshold', 0.6)) * 100
        
        for job in self.jobs_data:
            if not job['easy_apply']:
                continue
            
            analysis = await self.analyze_job_with_ai(job)
            
            job_with_analysis = {
                **job,
                'similarity_score': analysis['similarity_score'],
                'ai_decision': analysis['recommendation'],
                'ai_confidence': analysis['confidence'],
                'ai_reason': analysis['reasoning'],
                'matching_skills': analysis.get('matching_skills', []),
                'missing_skills': analysis.get('missing_skills', [])
            }
            
            if analysis['recommendation'] == 'APPLY' and analysis['similarity_score'] >= threshold:
                analyzed_jobs.append(job_with_analysis)
            
            await asyncio.sleep(random.uniform(2, 4))
        
        # Sort by score and take top N
        analyzed_jobs.sort(key=lambda x: x['similarity_score'], reverse=True)
        top_jobs = analyzed_jobs[:max_apply]
        
        print(f"✨ Selected {len(top_jobs)} jobs for application")
        for job in top_jobs:
            print(f"  • {job['title']} at {job['company']} - Score: {job['similarity_score']}%")
        
        return top_jobs
    
    async def auto_apply_job(self, job: Dict) -> Dict:
        """Automatically apply to a job"""
        print(f"\n🚀 Applying to: {job['title']} at {job['company']}")
        
        try:
            # Navigate to job
            await self.page.goto(job['url'])
            await asyncio.sleep(3)
            
            # Click Easy Apply button
            easy_apply_btn = await self.page.wait_for_selector(
                'button.jobs-apply-button',
                timeout=10000
            )
            await easy_apply_btn.click()
            await asyncio.sleep(2)
            
            # Handle multi-page application
            page_num = 1
            max_pages = 10
            
            while page_num <= max_pages:
                print(f"📄 Filling application page {page_num}...")
                
                # Fill all form fields on current page
                await self._fill_application_form()
                
                # Look for Next or Submit button
                try:
                    # Check for Review button first
                    review_btn = await self.page.query_selector('button[aria-label="Review your application"]')
                    if review_btn:
                        print("📝 Reviewing application...")
                        await review_btn.click()
                        await asyncio.sleep(2)
                        continue
                    
                    # Check for Submit button
                    submit_btn = await self.page.query_selector('button[aria-label*="Submit application"]')
                    if submit_btn:
                        print("✅ Submitting application...")
                        await submit_btn.click()
                        await asyncio.sleep(3)
                        
                        # Verify submission
                        if await self._verify_submission():
                            job['application_status'] = 'SUCCESS'
                            job['application_reason'] = 'Application submitted successfully'
                            print(f"🎉 Successfully applied to {job['title']}!")
                            self.applied_jobs.append(job)
                            return job
                        else:
                            raise Exception("Submission verification failed")
                    
                    # Check for Next button
                    next_btn = await self.page.query_selector('button[aria-label="Continue to next step"]')
                    if next_btn:
                        await next_btn.click()
                        await asyncio.sleep(2)
                        page_num += 1
                        continue
                    
                    # No more buttons, assume we're done
                    break
                    
                except Exception as e:
                    print(f"⚠️  Navigation error on page {page_num}: {str(e)}")
                    break
            
            # If we got here without success, mark as failed
            job['application_status'] = 'FAILED'
            job['application_reason'] = 'Could not complete application flow'
            return job
            
        except Exception as e:
            print(f"❌ Application error: {str(e)}")
            job['application_status'] = 'FAILED'
            job['application_reason'] = str(e)
            self.errors.append(f"Failed to apply to {job['title']}: {str(e)}")
            return job
    
    async def _fill_application_form(self) -> None:
        """Fill all fields on current application page"""
        try:
            # Get all input fields
            inputs = await self.page.query_selector_all('input[type="text"], input[type="tel"], input[type="email"]')
            
            for input_field in inputs:
                try:
                    label = await self._get_field_label(input_field)
                    value = await self._get_field_value(label)
                    
                    if value:
                        await input_field.fill(value)
                        await asyncio.sleep(random.uniform(0.5, 1))
                        print(f"  ✓ Filled: {label}")
                        
                except Exception as e:
                    print(f"  ⚠️  Could not fill field: {str(e)}")
            
            # Handle dropdowns
            selects = await self.page.query_selector_all('select')
            for select in selects:
                try:
                    label = await self._get_field_label(select)
                    # Select first non-empty option
                    options = await select.query_selector_all('option')
                    if len(options) > 1:
                        await options[1].click()
                        print(f"  ✓ Selected dropdown: {label}")
                except:
                    pass
            
            # Handle radio buttons (Yes for work authorization, No for sponsorship)
            radios = await self.page.query_selector_all('input[type="radio"]')
            for radio in radios:
                try:
                    label = await self._get_field_label(radio)
                    label_lower = label.lower()
                    
                    if 'authorized' in label_lower or 'eligible' in label_lower:
                        if 'yes' in label_lower:
                            await radio.click()
                            print(f"  ✓ Selected: Yes for work authorization")
                    elif 'sponsor' in label_lower:
                        if 'no' in label_lower:
                            await radio.click()
                            print(f"  ✓ Selected: No for sponsorship")
                            
                except:
                    pass
            
            # Handle checkboxes (check required ones)
            checkboxes = await self.page.query_selector_all('input[type="checkbox"]')
            for checkbox in checkboxes:
                try:
                    label = await self._get_field_label(checkbox)
                    if 'terms' in label.lower() or 'agree' in label.lower():
                        is_checked = await checkbox.is_checked()
                        if not is_checked:
                            await checkbox.click()
                            print(f"  ✓ Checked: {label}")
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️  Form filling error: {str(e)}")
    
    async def _get_field_label(self, element) -> str:
        """Get label text for a form field"""
        try:
            # Try to find associated label
            field_id = await element.get_attribute('id')
            if field_id:
                label = await self.page.query_selector(f'label[for="{field_id}"]')
                if label:
                    return await label.text_content()
            
            # Try aria-label
            aria_label = await element.get_attribute('aria-label')
            if aria_label:
                return aria_label
            
            # Try placeholder
            placeholder = await element.get_attribute('placeholder')
            if placeholder:
                return placeholder
            
            # Try name attribute
            name = await element.get_attribute('name')
            if name:
                return name
            
            return "Unknown field"
            
        except:
            return "Unknown field"
    
    async def _get_field_value(self, label: str) -> Optional[str]:
        """Get appropriate value for a field based on its label"""
        label_lower = label.lower()
        
        # Phone number
        if 'phone' in label_lower or 'mobile' in label_lower:
            return os.getenv('PHONE_NUMBER', '+1234567890')
        
        # Email
        if 'email' in label_lower:
            return os.getenv('LINKEDIN_EMAIL', '')
        
        # First name
        if 'first' in label_lower and 'name' in label_lower:
            return os.getenv('FIRST_NAME', 'John')
        
        # Last name
        if 'last' in label_lower and 'name' in label_lower:
            return os.getenv('LAST_NAME', 'Doe')
        
        # Years of experience
        if 'year' in label_lower and 'experience' in label_lower:
            return '5'
        
        # LinkedIn URL
        if 'linkedin' in label_lower and 'url' in label_lower:
            return os.getenv('LINKEDIN_URL', '')
        
        # Website
        if 'website' in label_lower or 'portfolio' in label_lower:
            return os.getenv('PORTFOLIO_URL', '')
        
        return None
    
    async def _verify_submission(self) -> bool:
        """Verify application was submitted successfully"""
        try:
            # Look for success indicators
            await asyncio.sleep(2)
            
            # Check for success message
            success_selectors = [
                'text="Application submitted"',
                'text="Your application was sent"',
                'text="successfully"',
                '[data-test-modal-id="application-submitted-modal"]'
            ]
            
            for selector in success_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=3000)
                    return True
                except:
                    continue
            
            # Check URL change
            if 'application-submitted' in self.page.url:
                return True
            
            return False
            
        except:
            return False
    
    def parse_resume(self, file_path: str) -> str:
        """Extract text from resume (supports PDF and TXT files)"""
        try:
            print(f"📄 Parsing resume: {file_path}")
            
            # Check file extension
            if file_path.endswith('.txt'):
                # Handle text files
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            elif file_path.endswith('.pdf'):
                # Handle PDF files
                with open(file_path, 'rb') as file:
                    pdf = PdfReader(file)
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            else:
                raise Exception(f"Unsupported file format: {file_path}")
            
            self.resume_text = text
            print(f"✅ Resume parsed: {len(text)} characters")
            return text
            
        except Exception as e:
            print(f"❌ Resume parsing error: {str(e)}")
            self.errors.append(f"Resume parsing failed: {str(e)}")
            return ""
    
    async def run_automation(self) -> Dict:
        """Main automation flow"""
        start_time = datetime.now()
        
        try:
            # Phase 1: Browser initialization
            print("\n" + "="*60)
            print("PHASE 1: BROWSER INITIALIZATION")
            print("="*60)
            await self.initialize_browser()
            
            # Phase 2: LinkedIn login
            print("\n" + "="*60)
            print("PHASE 2: LINKEDIN LOGIN")
            print("="*60)
            if not await self.login_linkedin():
                raise Exception("Login failed")
            
            # Phase 3: Parse resume
            print("\n" + "="*60)
            print("PHASE 3: RESUME PARSING")
            print("="*60)
            resume_path = self.config.get('resume_path', '')
            if resume_path:
                self.parse_resume(resume_path)
            
            # Phase 4: Job search
            print("\n" + "="*60)
            print("PHASE 4: JOB SEARCH")
            print("="*60)
            await self.search_jobs(
                self.config['keyword'],
                self.config['location']
            )
            
            # Phase 5: Collect job listings
            print("\n" + "="*60)
            print("PHASE 5: COLLECTING JOB LISTINGS")
            print("="*60)
            await self.collect_job_listings(max_jobs=30)
            
            # Phase 6: AI analysis and selection
            print("\n" + "="*60)
            print("PHASE 6: AI JOB ANALYSIS")
            print("="*60)
            max_apply = min(int(self.config.get('max_jobs', 5)), 5)  # Safety limit
            top_jobs = await self.select_top_jobs(max_apply=max_apply)
            
            # Phase 7: Auto-apply
            print("\n" + "="*60)
            print("PHASE 7: AUTOMATED APPLICATIONS")
            print("="*60)
            
            if self.config.get('auto_apply', True):
                for job in top_jobs:
                    result = await self.auto_apply_job(job)
                    await asyncio.sleep(random.uniform(10, 15))  # Delay between applications
            else:
                print("⏭️  Auto-apply disabled, skipping applications")
                for job in top_jobs:
                    job['application_status'] = 'SKIPPED'
                    job['application_reason'] = 'Auto-apply disabled'
            
            # Phase 8: Generate report
            print("\n" + "="*60)
            print("PHASE 8: GENERATING REPORT")
            print("="*60)
            
            end_time = datetime.now()
            duration = (end_time - start_time).seconds
            
            applications_successful = len([j for j in top_jobs if j.get('application_status') == 'SUCCESS'])
            
            report = {
                'jobs_found': len(self.jobs_data),
                'jobs_analyzed': len(self.jobs_data),
                'applications_attempted': len(top_jobs),
                'applications_successful': applications_successful,
                'jobs': top_jobs,
                'summary': f"Automation completed in {duration}s. Applied to {applications_successful}/{len(top_jobs)} jobs successfully.",
                'errors': self.errors,
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': duration
            }
            
            print("\n" + "="*60)
            print("✅ AUTOMATION COMPLETE!")
            print("="*60)
            print(f"📊 Jobs Found: {report['jobs_found']}")
            print(f"🤖 Jobs Analyzed: {report['jobs_analyzed']}")
            print(f"📝 Applications Attempted: {report['applications_attempted']}")
            print(f"✅ Applications Successful: {report['applications_successful']}")
            print(f"⏱️  Duration: {duration} seconds")
            
            return report
            
        except Exception as e:
            print(f"\n❌ AUTOMATION FAILED: {str(e)}")
            self.errors.append(f"Automation failed: {str(e)}")
            
            return {
                'jobs_found': len(self.jobs_data),
                'jobs_analyzed': len(self.jobs_data),
                'applications_attempted': 0,
                'applications_successful': 0,
                'jobs': [],
                'summary': f"Automation failed: {str(e)}",
                'errors': self.errors,
                'timestamp': datetime.now().isoformat()
            }
        
        finally:
            # Cleanup
            if self.browser:
                print("\n🧹 Cleaning up...")
                try:
                    await self.browser.close()
                except Exception as e:
                    print(f"⚠️  Browser cleanup warning: {str(e)}")
                    # Ignore cleanup errors as browser may already be closed
