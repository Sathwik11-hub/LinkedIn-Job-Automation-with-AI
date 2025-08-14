"""Cover letter generator service using OpenAI API."""

import json
from datetime import datetime
from typing import Dict, Optional
import openai

from ..core import LoggerMixin, get_settings
from ..models import ResumeData, JobPosting, CoverLetter


class CoverLetterGenerator(LoggerMixin):
    """Cover letter generator using OpenAI GPT."""
    
    def __init__(self):
        self.settings = get_settings()
        if self.settings.openai_api_key:
            openai.api_key = self.settings.openai_api_key
        else:
            self.logger.warning("OpenAI API key not configured")
    
    def generate_cover_letter(
        self, 
        job_posting: JobPosting, 
        resume_data: ResumeData,
        custom_template: Optional[str] = None
    ) -> CoverLetter:
        """Generate a personalized cover letter for the job."""
        self.logger.info(f"Generating cover letter for job: {job_posting.job_id}")
        
        try:
            # Create the prompt
            prompt = self._create_prompt(job_posting, resume_data, custom_template)
            
            # Generate cover letter using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career coach and professional writer specializing in creating compelling, personalized cover letters that help candidates stand out to employers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7,
                top_p=0.9
            )
            
            cover_letter_content = response.choices[0].message.content.strip()
            
            # Calculate personalization score
            personalization_score = self._calculate_personalization_score(
                cover_letter_content, job_posting, resume_data
            )
            
            cover_letter = CoverLetter(
                job_id=job_posting.job_id,
                content=cover_letter_content,
                personalization_score=personalization_score
            )
            
            self.logger.info(f"Cover letter generated with personalization score: {personalization_score:.2f}")
            return cover_letter
            
        except Exception as e:
            self.logger.error(f"Failed to generate cover letter: {str(e)}")
            # Fallback to template-based generation
            return self._generate_fallback_cover_letter(job_posting, resume_data)
    
    def _create_prompt(
        self, 
        job_posting: JobPosting, 
        resume_data: ResumeData,
        custom_template: Optional[str] = None
    ) -> str:
        """Create the prompt for cover letter generation."""
        # Extract relevant information
        skills_text = ", ".join(resume_data.skills) if resume_data.skills else "various technical skills"
        experience_text = self._format_experience(resume_data.experience)
        
        # Base prompt
        prompt = f"""
Write a professional, compelling cover letter for the following job application:

JOB DETAILS:
- Position: {job_posting.title}
- Company: {job_posting.company}
- Location: {job_posting.location}
- Job Description: {job_posting.description[:1000]}...

CANDIDATE PROFILE:
- Name: {resume_data.name or "[Your Name]"}
- Key Skills: {skills_text}
- Professional Summary: {resume_data.summary or "Experienced professional with diverse background"}
- Recent Experience: {experience_text}

REQUIREMENTS:
1. Write a personalized cover letter that specifically addresses this job and company
2. Highlight relevant skills and experience that match the job requirements
3. Show genuine interest in the company and role
4. Use a professional but engaging tone
5. Keep it concise (3-4 paragraphs, around 300-400 words)
6. Include specific examples from the candidate's background when possible
7. End with a strong call to action

FORMAT:
- Start with a compelling opening paragraph
- Include 1-2 body paragraphs highlighting relevant qualifications
- End with a professional closing paragraph
- Do not include address headers or dates
- Use [Your Name] for the signature if candidate name is not available

"""
        
        if custom_template:
            prompt += f"\nADDITIONAL INSTRUCTIONS:\n{custom_template}\n"
        
        return prompt
    
    def _format_experience(self, experience: list) -> str:
        """Format experience for the prompt."""
        if not experience:
            return "Diverse professional experience"
        
        # Take the most recent 2 experiences
        recent_exp = experience[:2]
        exp_texts = []
        
        for exp in recent_exp:
            title = exp.get('title', 'Professional Role')
            company = exp.get('company', 'Previous Company')
            description = exp.get('description', '')
            
            exp_text = f"{title} at {company}"
            if description:
                # Limit description length
                desc_short = description[:200] + "..." if len(description) > 200 else description
                exp_text += f" - {desc_short}"
            
            exp_texts.append(exp_text)
        
        return "; ".join(exp_texts)
    
    def _calculate_personalization_score(
        self, 
        cover_letter: str, 
        job_posting: JobPosting, 
        resume_data: ResumeData
    ) -> float:
        """Calculate how personalized the cover letter is."""
        score = 0.0
        cover_letter_lower = cover_letter.lower()
        
        # Check if company name is mentioned
        if job_posting.company.lower() in cover_letter_lower:
            score += 0.2
        
        # Check if job title is mentioned
        if job_posting.title.lower() in cover_letter_lower:
            score += 0.2
        
        # Check if candidate skills are mentioned
        skills_mentioned = 0
        for skill in resume_data.skills[:10]:  # Check top 10 skills
            if skill.lower() in cover_letter_lower:
                skills_mentioned += 1
        
        score += min(skills_mentioned / 10, 0.3)  # Up to 0.3 points for skills
        
        # Check if candidate name is used
        if resume_data.name and resume_data.name.lower() in cover_letter_lower:
            score += 0.1
        
        # Check length (appropriate length gets points)
        word_count = len(cover_letter.split())
        if 250 <= word_count <= 500:
            score += 0.2
        elif 200 <= word_count <= 600:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_fallback_cover_letter(
        self, 
        job_posting: JobPosting, 
        resume_data: ResumeData
    ) -> CoverLetter:
        """Generate a fallback cover letter using templates."""
        self.logger.info("Generating fallback cover letter using template")
        
        name = resume_data.name or "[Your Name]"
        skills = ", ".join(resume_data.skills[:5]) if resume_data.skills else "relevant technical skills"
        
        content = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_posting.title} position at {job_posting.company}. With my background in {skills} and proven experience in the technology sector, I am confident that I would be a valuable addition to your team.

In my previous roles, I have developed expertise in areas that directly align with your requirements. My technical skills include {skills}, which I have applied to deliver successful projects and drive innovation. I am particularly drawn to {job_posting.company} because of your commitment to excellence and your reputation in the industry.

I would welcome the opportunity to discuss how my background and enthusiasm can contribute to your team's continued success. Thank you for considering my application. I look forward to hearing from you soon.

Best regards,
{name}"""
        
        return CoverLetter(
            job_id=job_posting.job_id,
            content=content,
            personalization_score=0.5  # Medium score for template
        )
    
    def customize_cover_letter(
        self, 
        base_cover_letter: CoverLetter,
        customizations: Dict[str, str]
    ) -> CoverLetter:
        """Customize an existing cover letter with specific modifications."""
        content = base_cover_letter.content
        
        # Apply customizations
        for placeholder, replacement in customizations.items():
            content = content.replace(placeholder, replacement)
        
        # Recalculate personalization score (slightly lower for modified letters)
        new_score = base_cover_letter.personalization_score * 0.9
        
        return CoverLetter(
            job_id=base_cover_letter.job_id,
            content=content,
            personalization_score=new_score
        )
    
    def generate_multiple_variants(
        self, 
        job_posting: JobPosting, 
        resume_data: ResumeData,
        num_variants: int = 3
    ) -> list[CoverLetter]:
        """Generate multiple variants of cover letters for A/B testing."""
        variants = []
        
        templates = [
            None,  # Default approach
            "Focus more on technical achievements and quantifiable results",
            "Emphasize cultural fit and company values alignment",
            "Highlight leadership experience and team collaboration"
        ]
        
        for i in range(min(num_variants, len(templates))):
            try:
                variant = self.generate_cover_letter(
                    job_posting, 
                    resume_data, 
                    templates[i]
                )
                variants.append(variant)
            except Exception as e:
                self.logger.warning(f"Failed to generate variant {i+1}: {str(e)}")
        
        return variants