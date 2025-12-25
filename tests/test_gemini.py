#!/usr/bin/env python3
"""
Quick test for Gemini API integration
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_api():
    """Test Gemini API connection and cover letter generation."""
    print("🧪 Testing Gemini API Integration...")
    print("="*60)
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    # Test Gemini
    try:
        import google.generativeai as genai
        
        model = genai.GenerativeModel('gemini-2.5-flash', api_key=api_key)  # Pass API key directly
        
        print("\n📝 Generating test cover letter...")
        
        prompt = """
        Write a professional, concise cover letter for:
        
        Job Title: Senior AI Engineer
        Company: TechCorp
        Location: Remote
        
        Job Description: We're looking for an AI Engineer with Python and ML experience.
        
        Candidate Resume: 5+ years in AI/ML, expert in Python, TensorFlow, PyTorch.
        
        Requirements:
        - Maximum 150 words
        - Professional tone
        - Highlight relevant skills
        """
        
        response = model.generate_content(prompt)
        
        if response.text:
            print("\n✅ Cover Letter Generated Successfully!")
            print("="*60)
            print(response.text)
            print("="*60)
            print(f"\nWord count: {len(response.text.split())} words")
            return True
        else:
            print("❌ No response text received")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    exit(0 if success else 1)
