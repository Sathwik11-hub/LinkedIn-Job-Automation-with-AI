"""LinkedIn automation bot using Playwright (simplified).

This module provides a minimal bot to login, search jobs and apply automatically.
It is intentionally simple — for real use you'll need robust error handling,
rate limiting and compliance with LinkedIn's terms.
"""
from typing import Dict, Any, List
import asyncio

from playwright.async_api import async_playwright


class LinkedInBot:
    def __init__(self, email: str, password: str, headless: bool = True):
        self.email = email
        self.password = password
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()

    async def stop(self):
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception:
            pass

    async def login(self) -> bool:
        """Login to LinkedIn with credentials."""
        if not self.page:
            await self.start()
        
        print(f"🔐 Logging into LinkedIn as {self.email}...")
        await self.page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        await asyncio.sleep(2)
        
        try:
            # Fill in credentials
            print("📝 Entering credentials...")
            await self.page.fill('input[name="session_key"]', self.email)
            await self.page.fill('input[name="session_password"]', self.password)
            
            # Click login button
            print("🚀 Clicking login button...")
            await self.page.click('button[type="submit"]')
            
            # Wait for navigation
            await asyncio.sleep(5)
            
            # Check if login was successful
            current_url = self.page.url
            print(f"📍 Current URL: {current_url}")
            
            if "feed" in current_url or "mynetwork" in current_url or "jobs" in current_url:
                print("✅ Login successful!")
                return True
            elif "checkpoint" in current_url or "challenge" in current_url:
                print("⚠️ LinkedIn security checkpoint detected. Please complete it manually in the browser.")
                # Wait for user to complete checkpoint
                await asyncio.sleep(30)
                return "feed" in self.page.url
            else:
                print(f"❌ Login may have failed. Current URL: {current_url}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    async def search_jobs(self, keywords: str, location: str = "") -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn."""
        # Navigate to Jobs search
        q = keywords.replace(" ", "%20")
        loc = location.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search?keywords={q}&location={loc}&f_AL=true"  # f_AL=true for Easy Apply
        
        print(f"🔍 Searching for jobs: {keywords} in {location}")
        print(f"📍 URL: {url}")
        
        await self.page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)
        
        jobs = []
        # Try multiple selectors to find job cards
        print("📋 Extracting job listings...")
        
        try:
            # Try multiple approaches to wait for jobs to load
            selectors_to_try = [
                'ul.jobs-search__results-list',
                'div.jobs-search-results-list',
                'ul.scaffold-layout__list-container',
                'div.scaffold-layout__list',
                'ul[role="list"]'
            ]
            
            page_loaded = False
            for selector in selectors_to_try:
                try:
                    await self.page.wait_for_selector(selector, timeout=5000)
                    print(f"✅ Found jobs container: {selector}")
                    page_loaded = True
                    break
                except:
                    continue
            
            if not page_loaded:
                print("⚠️ Could not find jobs container, trying to extract anyway...")
            
            # Get all job cards using multiple possible selectors
            job_card_selectors = [
                'li.jobs-search-results__list-item',
                'div.job-card-container',
                'li.scaffold-layout__list-item',
                'div.jobs-search__job-card-container',
                'li[data-occludable-job-id]'
            ]
            
            job_cards = []
            for selector in job_card_selectors:
                cards = await self.page.query_selector_all(selector)
                if cards:
                    job_cards = cards
                    print(f"✅ Found {len(job_cards)} job cards using selector: {selector}")
                    break
            
            if not job_cards:
                print("❌ No job cards found with any selector")
                return jobs
            
            for idx, card in enumerate(job_cards[:10]):  # Get first 10 jobs
                try:
                    # Try multiple selectors for job link
                    link_selectors = [
                        'a.job-card-list__title',
                        'a.job-card-container__link',
                        'a[data-control-name="job_card_link"]',
                        'a.job-card-container__link-wrapper',
                        'h3.job-card-list__title a'
                    ]
                    
                    link_el = None
                    for link_sel in link_selectors:
                        link_el = await card.query_selector(link_sel)
                        if link_el:
                            break
                    
                    if link_el:
                        href = await link_el.get_attribute('href')
                        title_text = await link_el.inner_text()
                        
                        # Convert relative URL to absolute URL
                        if href and href.startswith('/'):
                            href = f"https://www.linkedin.com{href}"
                        
                        # Get company name with multiple selectors
                        company = "Unknown"
                        company_selectors = [
                            'span.job-card-container__company-name',
                            'a.job-card-container__company-name',
                            'h4.job-card-container__company-name',
                            'div.artdeco-entity-lockup__subtitle'
                        ]
                        
                        for comp_sel in company_selectors:
                            company_el = await card.query_selector(comp_sel)
                            if company_el:
                                company = await company_el.inner_text()
                                break
                        
                        jobs.append({
                            "title": title_text.strip(),
                            "company": company.strip(),
                            "url": href,
                            "index": idx + 1
                        })
                        print(f"  {idx + 1}. {title_text.strip()} at {company.strip()}")
                except Exception as e:
                    print(f"  ⚠️ Error extracting job {idx + 1}: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error searching jobs: {e}")
            
        print(f"✅ Total jobs found: {len(jobs)}")
        return jobs

    async def apply_to_job(self, job_url: str) -> Dict[str, Any]:
        # Deprecated: use prepare_application + submit_application instead
        return {"url": job_url, "status": "skipped", "note": "use prepare_application/submit_application"}

    async def prepare_application(self, job_url: str) -> Dict[str, Any]:
        """Navigate to the job and extract a preview of the application fields."""
        if not self.page:
            await self.start()
        await self.page.goto(job_url)
        await asyncio.sleep(1)
        preview = {"url": job_url, "title": "", "company": "", "fields": {}}
        try:
            if not self.page:
                await self.start()
            title_el = await self.page.query_selector('h1')
            if title_el:
                preview["title"] = (await title_el.inner_text()).strip()
            company_el = await self.page.query_selector('.topcard__org-name-link')
            if company_el:
                preview["company"] = (await company_el.inner_text()).strip()
            # Attempt to extract some input placeholders
            inputs = await self.page.query_selector_all('input, textarea, select')
            for i, inp in enumerate(inputs[:10]):
                try:
                    name = await inp.get_attribute('name') or await inp.get_attribute('id') or f'field_{i}'
                    placeholder = await inp.get_attribute('placeholder') or ''
                    preview['fields'][name] = placeholder
                except Exception:
                    continue
        except Exception:
            pass
        return preview

    async def submit_application(self, job_url: str) -> Dict[str, Any]:
        """Attempt to perform the Easy Apply submission (experimental).
        Returns a dict with status.
        """
        if not self.page:
            await self.start()
        await self.page.goto(job_url)
        await asyncio.sleep(1)
        result = {"url": job_url, "status": "skipped"}
        try:
            btn = await self.page.query_selector('button:has-text("Easy Apply")')
            if btn:
                await btn.click()
                await asyncio.sleep(1)
                # Naive submit
                submit = await self.page.query_selector('button:has-text("Submit")')
                if submit:
                    await submit.click()
                    await asyncio.sleep(1)
                    result["status"] = "applied"
                else:
                    result["status"] = "applied_partial"
            else:
                result["status"] = "no_easy_apply"
        except Exception:
            result["status"] = "error"
        return result
