"""
LLM-based cover letter generation service
"""

import asyncio
import openai
from typing import Dict, Any, Optional
from datetime import datetime

from app.models.job_schema import Job, Resume, CoverLetter
from app.services.resume_parser import ResumeParser
from app.config import settings
from app.utils.logger import setup_logger, log_async_performance

logger = setup_logger(__name__)


class CoverLetterGenerator:
    """
    AI-powered cover letter generator using LLM
    """
    
    def __init__(self):
        # Initialize OpenAI client if API key is available
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.llm_available = True
            logger.info("OpenAI client initialized")
        else:
            self.llm_available = False
            logger.warning("OpenAI API key not provided, using template-based generation")
        
        self.resume_parser = ResumeParser()
        
        # Default templates for different scenarios
        self.templates = {
            'standard': {
                'opening': "I am writing to express my strong interest in the {job_title} position at {company}.",
                'body': "With {years_experience} years of experience in {relevant_skills}, I am confident that my background aligns well with your requirements.",
                'closing': "I would welcome the opportunity to discuss how my skills and experience can contribute to {company}'s continued success."
            },
            'career_change': {
                'opening': "I am excited to apply for the {job_title} position at {company}, as I am eager to transition my skills into this field.",
                'body': "While my background is in {previous_field}, I have developed transferable skills in {relevant_skills} that would be valuable in this role.",
                'closing': "I am passionate about this career change and would appreciate the opportunity to discuss how my unique perspective can benefit {company}."
            },
            'entry_level': {
                'opening': "As a recent graduate with a passion for {field}, I am thrilled to apply for the {job_title} position at {company}.",
                'body': "Through my studies and {relevant_experience}, I have developed skills in {relevant_skills} and am eager to apply them in a professional setting.",
                'closing': "I am excited about the opportunity to grow with {company} and contribute fresh ideas to your team."
            }
        }
    
    @log_async_performance
    async def generate_cover_letter(
        self,
        job: Job,
        resume_path: str,
        template: Optional[str] = None,
        custom_instructions: Optional[str] = None
    ) -> CoverLetter:
        """
        Generate a personalized cover letter for a job application
        
        Args:
            job: Job posting information
            resume_path: Path to candidate's resume
            template: Template type to use ('standard', 'career_change', 'entry_level')
            custom_instructions: Additional instructions for customization
            
        Returns:
            Generated cover letter
        """
        try:
            # Parse resume
            resume = self.resume_parser.parse_resume(resume_path)
            logger.info(f"Generating cover letter for {resume.name} applying to {job.company}")
            
            # Generate cover letter content
            if self.llm_available:
                content = await self._generate_llm_cover_letter(job, resume, custom_instructions)
                model_used = settings.openai_model
            else:
                content = self._generate_template_cover_letter(job, resume, template or 'standard')
                model_used = "template_based"
            
            # Create cover letter object
            cover_letter = CoverLetter(
                job_id=job.id,
                content=content,
                model_used=model_used,
                prompt_template=template or 'standard',
                generated_at=datetime.utcnow()
            )
            
            # Calculate quality metrics
            cover_letter.relevance_score = self._calculate_relevance_score(content, job, resume)
            cover_letter.readability_score = self._calculate_readability_score(content)
            
            logger.info(f"Generated cover letter with relevance: {cover_letter.relevance_score:.2f}, readability: {cover_letter.readability_score:.2f}")
            
            return cover_letter
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            raise
    
    async def _generate_llm_cover_letter(
        self,
        job: Job,
        resume: Resume,
        custom_instructions: Optional[str] = None
    ) -> str:
        """Generate cover letter using LLM (OpenAI)"""
        
        # Build prompt
        prompt = self._build_llm_prompt(job, resume, custom_instructions)
        
        try:
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional career coach and expert cover letter writer. Write personalized, compelling cover letters that highlight relevant experience and skills while maintaining a professional tone."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Post-process to ensure proper formatting
            content = self._format_cover_letter(content, job, resume)
            
            return content
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            # Fallback to template-based generation
            return self._generate_template_cover_letter(job, resume, 'standard')
    
    def _build_llm_prompt(self, job: Job, resume: Resume, custom_instructions: Optional[str] = None) -> str:
        """Build prompt for LLM cover letter generation"""
        
        prompt = f"""
Write a professional cover letter for the following job application:

JOB DETAILS:
- Position: {job.title}
- Company: {job.company}
- Location: {job.location}
- Job Description: {job.description[:500]}...
- Required Skills: {', '.join(job.skills[:10])}

CANDIDATE DETAILS:
- Name: {resume.name}
- Years of Experience: {resume.years_experience or 0}
- Key Skills: {', '.join(resume.skills[:10])}
- Professional Summary: {resume.summary}
- Recent Experience: {resume.experience[0].get('title', 'Not specified') if resume.experience else 'Recent graduate'}

REQUIREMENTS:
- Keep it concise (3-4 paragraphs)
- Highlight relevant skills and experience that match the job requirements
- Show enthusiasm for the role and company
- Professional but engaging tone
- Include specific examples where possible
- End with a call to action

{f'ADDITIONAL INSTRUCTIONS: {custom_instructions}' if custom_instructions else ''}

Cover Letter:
"""
        
        return prompt
    
    def _generate_template_cover_letter(self, job: Job, resume: Resume, template_type: str) -> str:
        """Generate cover letter using templates"""
        
        template = self.templates.get(template_type, self.templates['standard'])
        
        # Extract relevant information
        relevant_skills = self._extract_relevant_skills(job, resume)
        years_exp = resume.years_experience or 0
        
        # Determine template type based on experience
        if years_exp == 0:
            template = self.templates['entry_level']
        elif years_exp > 10:
            template = self.templates['standard']
        
        # Fill template
        opening = template['opening'].format(
            job_title=job.title,
            company=job.company,
            field=self._extract_field_from_job(job)
        )
        
        body = template['body'].format(
            years_experience=years_exp,
            relevant_skills=', '.join(relevant_skills[:3]),
            previous_field=self._extract_field_from_resume(resume),
            relevant_experience="internships and projects" if years_exp == 0 else "professional experience"
        )
        
        closing = template['closing'].format(
            company=job.company
        )
        
        # Combine into full cover letter
        cover_letter = f"""Dear Hiring Manager,

{opening}

{body} {self._add_specific_achievements(resume)}

{closing}

Thank you for your time and consideration. I look forward to hearing from you.

Sincerely,
{resume.name}"""
        
        return cover_letter
    
    def _format_cover_letter(self, content: str, job: Job, resume: Resume) -> str:
        """Format and enhance cover letter content"""
        
        # Ensure proper header
        if not content.startswith("Dear"):
            content = f"Dear Hiring Manager,\n\n{content}"
        
        # Ensure proper closing
        if not content.endswith(resume.name):
            content = f"{content}\n\nSincerely,\n{resume.name}"
        
        # Clean up formatting
        content = content.replace('\n\n\n', '\n\n')
        content = content.strip()
        
        return content
    
    def _extract_relevant_skills(self, job: Job, resume: Resume) -> list[str]:
        """Extract skills from resume that are relevant to the job"""
        
        job_skills = set([skill.lower() for skill in job.skills])
        resume_skills = set([skill.lower() for skill in resume.skills])
        
        # Find matching skills
        matching_skills = job_skills.intersection(resume_skills)
        
        # If not enough matches, include top resume skills
        relevant_skills = list(matching_skills)
        if len(relevant_skills) < 3:
            additional_skills = [skill for skill in resume.skills if skill.lower() not in matching_skills]
            relevant_skills.extend(additional_skills[:3-len(relevant_skills)])
        
        return relevant_skills[:5]
    
    def _extract_field_from_job(self, job: Job) -> str:
        """Extract field/industry from job information"""
        
        # Simple keyword matching
        tech_keywords = ['software', 'developer', 'engineer', 'technical', 'programming']
        business_keywords = ['marketing', 'sales', 'business', 'manager', 'analyst']
        data_keywords = ['data', 'scientist', 'analytics', 'machine learning', 'ai']
        
        job_text = f"{job.title} {job.description}".lower()
        
        if any(keyword in job_text for keyword in data_keywords):
            return "data science and analytics"
        elif any(keyword in job_text for keyword in tech_keywords):
            return "technology"
        elif any(keyword in job_text for keyword in business_keywords):
            return "business"
        else:
            return "this field"
    
    def _extract_field_from_resume(self, resume: Resume) -> str:
        """Extract primary field from resume"""
        
        # Look at most recent experience
        if resume.experience:
            recent_title = resume.experience[0].get('title', '').lower()
            
            if any(keyword in recent_title for keyword in ['engineer', 'developer', 'technical']):
                return "technology"
            elif any(keyword in recent_title for keyword in ['analyst', 'data', 'scientist']):
                return "analytics"
            elif any(keyword in recent_title for keyword in ['marketing', 'business', 'sales']):
                return "business"
        
        return "my previous field"
    
    def _add_specific_achievements(self, resume: Resume) -> str:
        """Add specific achievements to the cover letter"""
        
        if resume.key_achievements:
            achievement = resume.key_achievements[0]
            return f" For example, I {achievement.lower()}."
        
        return ""
    
    def _calculate_relevance_score(self, content: str, job: Job, resume: Resume) -> float:
        """Calculate how relevant the cover letter is to the job"""
        
        content_lower = content.lower()
        score = 0.0
        
        # Check if job title is mentioned
        if job.title.lower() in content_lower:
            score += 0.2
        
        # Check if company is mentioned
        if job.company.lower() in content_lower:
            score += 0.2
        
        # Check for skill mentions
        job_skills = [skill.lower() for skill in job.skills]
        mentioned_skills = sum(1 for skill in job_skills if skill in content_lower)
        score += min(mentioned_skills / len(job_skills), 0.3) if job_skills else 0
        
        # Check for experience mentions
        if str(resume.years_experience or 0) in content:
            score += 0.1
        
        # Check for specific achievements/numbers
        import re
        if re.search(r'\d+%|\$\d+|\d+\s*(users|customers|projects)', content_lower):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_readability_score(self, content: str) -> float:
        """Calculate readability score (simplified)"""
        
        sentences = content.split('.')
        words = content.split()
        
        if not sentences or not words:
            return 0.0
        
        # Average words per sentence (ideal: 15-20)
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Penalize very long or very short sentences
        if 15 <= avg_words_per_sentence <= 20:
            sentence_score = 1.0
        elif 10 <= avg_words_per_sentence < 15 or 20 < avg_words_per_sentence <= 25:
            sentence_score = 0.8
        else:
            sentence_score = 0.6
        
        # Check for variety in sentence starts
        sentence_starts = [sent.strip()[:10] for sent in sentences if sent.strip()]
        unique_starts = len(set(sentence_starts))
        variety_score = min(unique_starts / len(sentence_starts), 1.0) if sentence_starts else 0
        
        # Overall readability
        readability = (sentence_score * 0.7) + (variety_score * 0.3)
        
        return readability
    
    async def generate_multiple_versions(
        self,
        job: Job,
        resume_path: str,
        count: int = 3
    ) -> list[CoverLetter]:
        """Generate multiple versions of cover letter for A/B testing"""
        
        cover_letters = []
        templates = ['standard', 'career_change', 'entry_level']
        
        for i in range(min(count, len(templates))):
            try:
                template = templates[i] if i < len(templates) else 'standard'
                cover_letter = await self.generate_cover_letter(
                    job, 
                    resume_path, 
                    template=template,
                    custom_instructions=f"Version {i+1}: Use a {'more formal' if i == 0 else 'more conversational' if i == 1 else 'more enthusiastic'} tone"
                )
                cover_letters.append(cover_letter)
            except Exception as e:
                logger.warning(f"Error generating cover letter version {i+1}: {e}")
        
        return cover_letters
    
    def customize_for_company(self, base_cover_letter: str, company_info: Dict[str, Any]) -> str:
        """Customize cover letter with specific company information"""
        
        # Add company-specific information if available
        customizations = []
        
        if company_info.get('mission'):
            customizations.append(f"I am particularly drawn to {company_info['company']}'s mission of {company_info['mission']}.")
        
        if company_info.get('recent_news'):
            customizations.append(f"I was excited to learn about {company_info['recent_news']}.")
        
        if company_info.get('values'):
            customizations.append(f"Your company's focus on {company_info['values']} aligns perfectly with my own values.")
        
        # Insert customizations into the cover letter
        if customizations:
            paragraphs = base_cover_letter.split('\n\n')
            # Insert after the first paragraph
            if len(paragraphs) > 1:
                paragraphs.insert(2, ' '.join(customizations))
                return '\n\n'.join(paragraphs)
        
        return base_cover_letter