from playwright.async_api import Page
from typing import Dict, List, Optional
import asyncio
import random

class FormFiller:
    """Automated form filling service for job applications"""
    
    def __init__(self, page: Page):
        self.page = page
    
    async def fill_application_form(self, form_data: Dict) -> Dict:
        """Fill out a job application form automatically"""
        try:
            results = {
                "fields_filled": [],
                "fields_failed": [],
                "success": True
            }
            
            # Common form field patterns and their data mappings
            field_mappings = {
                # Personal Information
                "first_name": ["first.name", "firstName", "fname", "given.name"],
                "last_name": ["last.name", "lastName", "lname", "family.name", "surname"],
                "email": ["email", "emailAddress", "email.address"],
                "phone": ["phone", "phoneNumber", "phone.number", "mobile", "telephone"],
                
                # Experience and Education
                "years_experience": ["experience", "years.experience", "total.experience"],
                "current_company": ["current.company", "currentCompany", "employer"],
                "current_title": ["current.title", "currentTitle", "job.title"],
                "education_level": ["education", "degree", "education.level"],
                "university": ["university", "school", "college", "institution"],
                
                # Application specific
                "cover_letter": ["cover.letter", "coverLetter", "message", "additional.info"],
                "salary_expectation": ["salary", "expected.salary", "salary.expectation"],
                "availability": ["start.date", "availability", "notice.period"],
                "work_authorization": ["work.authorization", "visa.status", "authorization"],
                "location": ["location", "preferred.location", "city", "address"]
            }
            
            # Fill each field type
            for field_type, selectors in field_mappings.items():
                if field_type in form_data:
                    success = await self._fill_field(
                        selectors, 
                        form_data[field_type], 
                        field_type
                    )
                    
                    if success:
                        results["fields_filled"].append(field_type)
                    else:
                        results["fields_failed"].append(field_type)
            
            # Handle file uploads (resume, cover letter)
            if "resume_path" in form_data:
                upload_success = await self._handle_file_upload(
                    ["resume", "cv", "upload"], 
                    form_data["resume_path"]
                )
                if upload_success:
                    results["fields_filled"].append("resume_upload")
                else:
                    results["fields_failed"].append("resume_upload")
            
            # Handle dropdowns and select fields
            await self._handle_dropdown_fields(form_data, results)
            
            # Handle checkboxes and radio buttons
            await self._handle_checkbox_fields(form_data, results)
            
            return results
            
        except Exception as e:
            return {
                "fields_filled": [],
                "fields_failed": ["form_filling_error"],
                "success": False,
                "error": str(e)
            }
    
    async def _fill_field(self, selectors: List[str], value: str, field_type: str) -> bool:
        """Fill a specific field using multiple selector strategies"""
        try:
            for selector_pattern in selectors:
                # Try different selector strategies
                selectors_to_try = [
                    f"input[name*='{selector_pattern}']",
                    f"input[id*='{selector_pattern}']",
                    f"input[placeholder*='{selector_pattern}']",
                    f"textarea[name*='{selector_pattern}']",
                    f"textarea[id*='{selector_pattern}']",
                    f"[data-testid*='{selector_pattern}']",
                    f"[aria-label*='{selector_pattern}']"
                ]
                
                for selector in selectors_to_try:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            # Check if element is visible and enabled
                            is_visible = await element.is_visible()
                            is_enabled = await element.is_enabled()
                            
                            if is_visible and is_enabled:
                                await element.fill(str(value))
                                await self._random_delay(0.5, 1.5)
                                return True
                                
                    except Exception:
                        continue
            
            return False
            
        except Exception:
            return False
    
    async def _handle_file_upload(self, file_selectors: List[str], file_path: str) -> bool:
        """Handle file upload fields"""
        try:
            for selector_pattern in file_selectors:
                selectors_to_try = [
                    f"input[type='file'][name*='{selector_pattern}']",
                    f"input[type='file'][id*='{selector_pattern}']",
                    f"input[type='file'][accept*='pdf']",
                    "input[type='file']"
                ]
                
                for selector in selectors_to_try:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            await element.set_input_files(file_path)
                            await self._random_delay(1, 2)
                            return True
                    except Exception:
                        continue
            
            return False
            
        except Exception:
            return False
    
    async def _handle_dropdown_fields(self, form_data: Dict, results: Dict):
        """Handle dropdown/select fields"""
        dropdown_mappings = {
            "experience_level": ["Entry level", "Mid level", "Senior", "Executive"],
            "job_type": ["Full-time", "Part-time", "Contract", "Internship"],
            "education_level": ["High School", "Bachelor's", "Master's", "PhD"],
            "work_authorization": ["Yes", "No", "Require Sponsorship"]
        }
        
        for field, options in dropdown_mappings.items():
            if field in form_data:
                try:
                    # Find select elements
                    selects = await self.page.query_selector_all("select")
                    
                    for select in selects:
                        # Check if this select might be for this field
                        name = await select.get_attribute("name") or ""
                        id_attr = await select.get_attribute("id") or ""
                        
                        if field.replace("_", "") in name.lower() or field.replace("_", "") in id_attr.lower():
                            # Try to select the appropriate option
                            user_value = str(form_data[field]).lower()
                            
                            for option in options:
                                if user_value in option.lower() or option.lower() in user_value:
                                    await select.select_option(label=option)
                                    results["fields_filled"].append(f"{field}_dropdown")
                                    break
                            break
                
                except Exception:
                    results["fields_failed"].append(f"{field}_dropdown")
    
    async def _handle_checkbox_fields(self, form_data: Dict, results: Dict):
        """Handle checkbox and radio button fields"""
        checkbox_fields = {
            "terms_accepted": True,
            "privacy_policy": True,
            "newsletter_subscribe": False,
            "remote_work": form_data.get("remote_preference", False),
            "willing_to_relocate": form_data.get("relocation_ok", False)
        }
        
        for field, should_check in checkbox_fields.items():
            try:
                # Look for checkboxes related to this field
                checkboxes = await self.page.query_selector_all("input[type='checkbox']")
                
                for checkbox in checkboxes:
                    name = await checkbox.get_attribute("name") or ""
                    id_attr = await checkbox.get_attribute("id") or ""
                    
                    field_keywords = field.replace("_", "").lower()
                    
                    if field_keywords in name.lower() or field_keywords in id_attr.lower():
                        is_checked = await checkbox.is_checked()
                        
                        if should_check and not is_checked:
                            await checkbox.click()
                            results["fields_filled"].append(f"{field}_checkbox")
                        elif not should_check and is_checked:
                            await checkbox.click()
                            results["fields_filled"].append(f"{field}_checkbox")
                        break
                        
            except Exception:
                results["fields_failed"].append(f"{field}_checkbox")
    
    async def find_and_click_submit(self) -> bool:
        """Find and click the submit button"""
        try:
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button[aria-label*='Submit']",
                "button[aria-label*='Apply']",
                "button:has-text('Submit')",
                "button:has-text('Apply')",
                "button:has-text('Send')",
                "[data-testid*='submit']",
                "[data-testid*='apply']"
            ]
            
            for selector in submit_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element:
                        is_visible = await element.is_visible()
                        is_enabled = await element.is_enabled()
                        
                        if is_visible and is_enabled:
                            await element.click()
                            await self._random_delay(2, 4)
                            return True
                            
                except Exception:
                    continue
            
            return False
            
        except Exception:
            return False
    
    async def detect_form_errors(self) -> List[str]:
        """Detect any form validation errors"""
        try:
            error_selectors = [
                ".error",
                ".field-error",
                ".form-error",
                "[aria-invalid='true']",
                ".validation-error",
                ".input-error"
            ]
            
            errors = []
            
            for selector in error_selectors:
                error_elements = await self.page.query_selector_all(selector)
                
                for element in error_elements:
                    if await element.is_visible():
                        error_text = await element.inner_text()
                        if error_text and error_text.strip():
                            errors.append(error_text.strip())
            
            return errors
            
        except Exception:
            return []
    
    async def _random_delay(self, min_seconds: float, max_seconds: float):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)