import openai
import asyncio
from typing import List, Dict, Optional
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def generate_cover_letter(
        self, 
        job_description: str, 
        resume_content: str, 
        user_name: str = "Job Applicant"
    ) -> str:
        """Generate a personalized cover letter using AI"""
        prompt = f"""
        Write a professional cover letter for the following job application:
        
        Job Description:
        {job_description}
        
        Applicant's Resume/Background:
        {resume_content}
        
        Applicant Name: {user_name}
        
        Guidelines:
        - Keep it concise (3-4 paragraphs)
        - Highlight relevant skills and experience
        - Show enthusiasm for the role
        - Use professional tone
        - Customize it to the specific job and company
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional career advisor helping write effective cover letters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return self._get_fallback_cover_letter(user_name)
    
    async def analyze_job_fit(self, job_description: str, skills: List[str]) -> Dict:
        """Analyze how well user skills match a job description"""
        skills_text = ", ".join(skills)
        prompt = f"""
        Analyze the job-skill match between the candidate's skills and job requirements:
        
        Job Description:
        {job_description}
        
        Candidate Skills:
        {skills_text}
        
        Provide a JSON response with:
        1. match_score (0-100)
        2. matching_skills (list of skills that match)
        3. missing_skills (list of required skills candidate lacks)
        4. recommendations (list of suggestions)
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI career counselor. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            # Parse JSON response
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error analyzing job fit: {e}")
            return {
                "match_score": 50,
                "matching_skills": [],
                "missing_skills": [],
                "recommendations": ["Unable to analyze at this time"]
            }
    
    async def extract_job_requirements(self, job_description: str) -> Dict:
        """Extract structured information from job description"""
        prompt = f"""
        Extract key information from this job description and return as JSON:
        
        {job_description}
        
        Extract:
        1. required_skills (list)
        2. preferred_skills (list)
        3. experience_years (number or range)
        4. education_requirements (string)
        5. key_responsibilities (list)
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an HR assistant. Extract job information and respond in valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error extracting job requirements: {e}")
            return {
                "required_skills": [],
                "preferred_skills": [],
                "experience_years": "Not specified",
                "education_requirements": "Not specified",
                "key_responsibilities": []
            }
    
    def _get_fallback_cover_letter(self, user_name: str) -> str:
        """Fallback cover letter template"""
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the position at your company. With my background and skills, I believe I would be a valuable addition to your team.

I am excited about the opportunity to contribute to your organization and would welcome the chance to discuss how my experience aligns with your needs.

Thank you for your consideration. I look forward to hearing from you.

Sincerely,
{user_name}"""