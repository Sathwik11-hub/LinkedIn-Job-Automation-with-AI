#!/usr/bin/env python3
"""
LinkedIn Auto Apply - Quick Test Script
This script helps you test the automation without running a full session.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_auto_apply import LinkedInAutoApply
from dotenv import load_dotenv

# Load environment
load_dotenv()


async def test_browser_init():
    """Test 1: Browser initialization."""
    print("\n" + "="*60)
    print("TEST 1: Browser Initialization")
    print("="*60)
    
    try:
        agent = LinkedInAutoApply(
            email=os.getenv('LINKEDIN_EMAIL', 'test@example.com'),
            password=os.getenv('LINKEDIN_PASSWORD', 'password'),
            resume_path='./data/resumes/test_resume.txt',
            headless=False,
            use_llm=False
        )
        
        print("✅ LinkedInAutoApply instance created")
        
        await agent.initialize_browser()
        print("✅ Browser initialized successfully")
        
        print(f"📄 Browser: {agent.browser}")
        print(f"📄 Page: {agent.page}")
        
        await agent.cleanup()
        print("✅ Browser cleanup successful")
        
        return True
    
    except Exception as e:
        print(f"❌ Browser initialization failed: {e}")
        return False


async def test_login():
    """Test 2: LinkedIn login."""
    print("\n" + "="*60)
    print("TEST 2: LinkedIn Login")
    print("="*60)
    
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("⚠️  Skipping login test - credentials not configured")
        print("   Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")
        return False
    
    try:
        agent = LinkedInAutoApply(
            email=email,
            password=password,
            resume_path='./data/resumes/test_resume.txt',
            headless=False,
            use_llm=False
        )
        
        await agent.initialize_browser()
        print("✅ Browser initialized")
        
        login_success = await agent.login_linkedin()
        
        if login_success:
            print("✅ LinkedIn login successful")
            print(f"📄 Current URL: {agent.page.url}")
        else:
            print("❌ LinkedIn login failed")
        
        await asyncio.sleep(5)  # Wait to verify login
        await agent.cleanup()
        
        return login_success
    
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False


async def test_resume_parsing():
    """Test 3: Resume parsing."""
    print("\n" + "="*60)
    print("TEST 3: Resume Parsing")
    print("="*60)
    
    # Create test resume if not exists
    test_resume = Path('./data/resumes/test_resume.txt')
    test_resume.parent.mkdir(parents=True, exist_ok=True)
    
    if not test_resume.exists():
        print("Creating test resume...")
        test_resume.write_text("""
John Doe
AI Engineer

Skills:
- Python, JavaScript, Java
- Machine Learning, Deep Learning
- TensorFlow, PyTorch, scikit-learn
- FastAPI, Django, Flask
- AWS, Docker, Kubernetes
- SQL, MongoDB, PostgreSQL

Experience:
5+ years in AI/ML engineering
Built production ML systems
Led team of 3 engineers
        """)
    
    try:
        agent = LinkedInAutoApply(
            email='test@example.com',
            password='password',
            resume_path=str(test_resume),
            headless=True,
            use_llm=False
        )
        
        print(f"✅ Resume loaded: {len(agent.resume_text)} characters")
        print(f"✅ Keywords extracted: {len(agent.resume_keywords)} keywords")
        print(f"📝 Sample keywords: {agent.resume_keywords[:10]}")
        
        return True
    
    except Exception as e:
        print(f"❌ Resume parsing failed: {e}")
        return False


async def test_job_matching():
    """Test 4: Job matching algorithm."""
    print("\n" + "="*60)
    print("TEST 4: Job Matching Algorithm")
    print("="*60)
    
    from linkedin_auto_apply import JobListing
    
    test_resume = Path('./data/resumes/test_resume.txt')
    if not test_resume.exists():
        print("⚠️  Test resume not found. Run test_resume_parsing first.")
        return False
    
    try:
        agent = LinkedInAutoApply(
            email='test@example.com',
            password='password',
            resume_path=str(test_resume),
            headless=True,
            use_llm=False
        )
        
        # Test job 1: Good match
        job1 = JobListing(
            job_id="1",
            title="Senior AI Engineer",
            company="TechCorp",
            location="Remote",
            description="""
            We are looking for a Senior AI Engineer with strong Python skills.
            You will work on machine learning systems using TensorFlow and PyTorch.
            Experience with FastAPI and AWS is required.
            Docker and Kubernetes knowledge is a plus.
            """,
            apply_link="https://example.com/job1"
        )
        
        score1, keywords1 = agent.analyze_job_fit(job1)
        print(f"\nJob 1: {job1.title}")
        print(f"  Match Score: {score1:.1f}%")
        print(f"  Keywords Matched: {len(keywords1)}")
        print(f"  Sample Keywords: {keywords1[:5]}")
        
        # Test job 2: Poor match
        job2 = JobListing(
            job_id="2",
            title="Sales Manager",
            company="SalesCo",
            location="New York",
            description="""
            We are looking for an experienced Sales Manager.
            You will manage a team and close deals.
            CRM experience required.
            """,
            apply_link="https://example.com/job2"
        )
        
        score2, keywords2 = agent.analyze_job_fit(job2)
        print(f"\nJob 2: {job2.title}")
        print(f"  Match Score: {score2:.1f}%")
        print(f"  Keywords Matched: {len(keywords2)}")
        
        if score1 > score2:
            print(f"\n✅ Matching algorithm working correctly")
            print(f"   AI job scored {score1:.1f}% vs Sales job {score2:.1f}%")
            return True
        else:
            print(f"\n❌ Matching algorithm may need tuning")
            return False
    
    except Exception as e:
        print(f"❌ Job matching test failed: {e}")
        return False


async def test_llm_integration():
    """Test 5: LLM cover letter generation."""
    print("\n" + "="*60)
    print("TEST 5: LLM Cover Letter Generation")
    print("="*60)
    
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not openai_key and not gemini_key:
        print("⚠️  Skipping LLM test - no API keys configured")
        print("   Set OPENAI_API_KEY or GEMINI_API_KEY in .env")
        return False
    
    from linkedin_auto_apply import JobListing
    
    test_resume = Path('./data/resumes/test_resume.txt')
    if not test_resume.exists():
        print("⚠️  Test resume not found.")
        return False
    
    try:
        agent = LinkedInAutoApply(
            email='test@example.com',
            password='password',
            resume_path=str(test_resume),
            headless=True,
            use_llm=True
        )
        
        test_job = JobListing(
            job_id="1",
            title="Senior AI Engineer",
            company="TechCorp",
            location="Remote",
            description="Building AI systems with Python and ML.",
            apply_link="https://example.com/job"
        )
        
        print("Generating cover letter...")
        cover_letter = await agent.generate_cover_letter(test_job)
        
        if cover_letter:
            print("✅ Cover letter generated successfully")
            print(f"\n{'-'*60}")
            print(cover_letter)
            print(f"{'-'*60}\n")
            print(f"Length: {len(cover_letter)} characters")
            print(f"Word count: {len(cover_letter.split())} words")
            return True
        else:
            print("❌ Cover letter generation returned None")
            return False
    
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False


async def test_report_generation():
    """Test 6: Report generation."""
    print("\n" + "="*60)
    print("TEST 6: Report Generation")
    print("="*60)
    
    from linkedin_auto_apply import JobListing, ApplicationResult
    from datetime import datetime
    
    test_resume = Path('./data/resumes/test_resume.txt')
    if not test_resume.exists():
        print("⚠️  Test resume not found.")
        return False
    
    try:
        agent = LinkedInAutoApply(
            email='test@example.com',
            password='password',
            resume_path=str(test_resume),
            headless=True,
            use_llm=False
        )
        
        # Create test data
        agent.jobs_found = [
            JobListing(
                job_id=f"{i}",
                title=f"AI Engineer {i}",
                company=f"Company {i}",
                location="Remote",
                description="Python ML AI",
                apply_link=f"https://example.com/{i}",
                match_score=85.0 - i*5,
                keywords_matched=["python", "ml", "ai"]
            )
            for i in range(5)
        ]
        
        agent.jobs_applied = [
            ApplicationResult(
                job_id="1",
                job_title="AI Engineer 1",
                company="Company 1",
                status="success",
                timestamp=datetime.now().isoformat(),
                cover_letter_generated=True
            ),
            ApplicationResult(
                job_id="2",
                job_title="AI Engineer 2",
                company="Company 2",
                status="success",
                timestamp=datetime.now().isoformat(),
                cover_letter_generated=True
            )
        ]
        
        # Generate report
        report = agent.generate_report()
        
        print("✅ Report generated successfully")
        print(f"\n{'-'*60}")
        agent.print_console_report(report)
        print(f"{'-'*60}\n")
        
        print(f"✅ Report saved to: reports/")
        
        return True
    
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests."""
    print("\n")
    print("="*60)
    print("🧪 LINKEDIN AUTO APPLY - TEST SUITE")
    print("="*60)
    print("\nRunning comprehensive tests...")
    
    results = {}
    
    # Test 1: Browser initialization
    results['browser_init'] = await test_browser_init()
    
    # Test 2: LinkedIn login (optional, requires credentials)
    results['login'] = await test_login()
    
    # Test 3: Resume parsing
    results['resume_parsing'] = await test_resume_parsing()
    
    # Test 4: Job matching
    results['job_matching'] = await test_job_matching()
    
    # Test 5: LLM integration (optional, requires API key)
    results['llm_integration'] = await test_llm_integration()
    
    # Test 6: Report generation
    results['report_generation'] = await test_report_generation()
    
    # Summary
    print("\n")
    print("="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    elif passed >= total * 0.7:
        print("⚠️  Most tests passed. Check failed tests before using.")
    else:
        print("❌ Multiple tests failed. Please fix issues before using.")
    
    return passed == total


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 LinkedIn Auto Apply - Test Suite                  ║
║                                                              ║
║  This script will run comprehensive tests to verify         ║
║  the automation system is working correctly.                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
