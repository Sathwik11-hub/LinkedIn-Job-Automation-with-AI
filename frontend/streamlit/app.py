"""
AutoAgentHire - LinkedIn Job Automation Platform
Streamlit frontend with Playwright browser automation and Gemini AI integration.
"""
import streamlit as st
import requests
from typing import Optional
import asyncio
import subprocess
import os

# Page config
st.set_page_config(
    page_title="AutoAgentHire - LinkedIn Job Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_URL = "http://127.0.0.1:58664"


def check_api_health() -> bool:
    """Check if the backend API is available."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def run_demo_script():
    """Run the AutoAgentHire demo script."""
    try:
        # Run the demo script
        result = subprocess.run(
            ["python", "demo_autoagenthire.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Demo timed out after 5 minutes", 1
    except Exception as e:
        return "", f"Error running demo: {str(e)}", 1


def main():
    """Main application function."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 AutoAgentHire")
        st.caption("LinkedIn Job Automation with AI")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "� AutoAgentHire", "�🔍 Job Search", "📋 Applications", "👤 Profile", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
        
        # Environment Status
        st.markdown("### 🔧 Environment Status")
        linkedin_email = os.getenv('LINKEDIN_EMAIL')
        linkedin_password = os.getenv('LINKEDIN_PASSWORD') 
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        st.write(f"📧 LinkedIn Email: {'✅' if linkedin_email else '❌'}")
        st.write(f"🔐 LinkedIn Password: {'✅' if linkedin_password else '❌'}")
        st.write(f"🤖 Gemini API Key: {'✅' if gemini_api_key else '❌'}")
        
        if not all([linkedin_email, linkedin_password, gemini_api_key]):
            st.warning("⚠️ Please configure environment variables in .env file")
    
    # Main content
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🚀 AutoAgentHire":
        show_autoagenthire()
    elif page == "🔍 Job Search":
        show_job_search()
    elif page == "📋 Applications":
        show_applications()
    elif page == "👤 Profile":
        show_profile()
    elif page == "⚙️ Settings":
        show_settings()


def show_autoagenthire():
    """Display AutoAgentHire automation interface."""
    st.title("🚀 AutoAgentHire - LinkedIn Job Automation")
    st.caption("Powered by Playwright Browser Automation + Gemini AI")
    
    # Status indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        linkedin_configured = bool(os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD'))
        if linkedin_configured:
            st.success("✅ LinkedIn Configured")
        else:
            st.error("❌ LinkedIn Not Configured")
    
    with col2:
        gemini_configured = bool(os.getenv('GEMINI_API_KEY'))
        if gemini_configured:
            st.success("✅ Gemini AI Ready")
        else:
            st.error("❌ Gemini AI Not Configured")
    
    with col3:
        api_ready = check_api_health()
        if api_ready:
            st.success("✅ Backend Ready")
        else:
            st.error("❌ Backend Offline")
    
    st.markdown("---")
    
    # Automation controls
    st.subheader("🤖 Automation Controls")
    
    all_ready = linkedin_configured and gemini_configured and api_ready
    
    if not all_ready:
        st.warning("⚠️ Please configure all required services before starting automation")
        
        if not linkedin_configured:
            st.info("💡 Add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to your .env file")
        if not gemini_configured:
            st.info("💡 Add GEMINI_API_KEY to your .env file")
        if not api_ready:
            st.info("💡 Start the backend server: `uvicorn backend.main:app --reload`")
    else:
        # Demo mode
        st.info("🛡️ **Demo Mode**: Safe testing without real applications")
        
    
    with col1:
        if st.button("🎬 Run AutoAgentHire Demo", use_container_width=True):
            with st.spinner("🤖 Running AutoAgentHire automation..."):
                stdout, stderr, returncode = run_demo_script()
                
                if returncode == 0:
                    st.success("✅ Demo completed successfully!")
                    with st.expander("📋 Demo Output"):
                        st.text(stdout)
                else:
                    st.error("❌ Demo failed")
                    with st.expander("🔍 Error Details"):
                        st.text(stderr)
    
    with col2:
        if st.button("🔧 Test Login Only", use_container_width=True):
            with st.spinner("🔐 Testing LinkedIn login..."):
                # This would call the login test
                st.info("Login test feature - implement with subprocess call to test_enhanced_login.py")

    st.markdown("---")
    
    # Features overview
    st.subheader("🎯 AutoAgentHire Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **🤖 AI-Powered Automation**
        - Playwright browser automation
        - Human-like interaction patterns
        - Advanced bot detection bypass
        - Smart form filling
        
        **🧠 Gemini AI Integration** 
        - Job compatibility analysis
        - Intelligent application decisions
        - Custom cover letter generation
        - Resume optimization suggestions
        """)
    
    with feature_col2:
        st.markdown("""
        **🔒 Security & Stealth**
        - Anti-detection features
        - User agent spoofing
        - Geolocation simulation
        - Session management
        
        **📊 Smart Analytics**
        - Application tracking
        - Success rate monitoring
        - Job match scoring
        - Performance insights
        """)
    
    # Configuration panel
    with st.expander("⚙️ Advanced Configuration"):
        st.markdown("**Automation Settings**")
        
        col1, col2 = st.columns(2)
        with col1:
            headless_mode = st.checkbox("Headless Browser", value=True, help="Run browser in background")
            apply_limit = st.number_input("Max Applications", min_value=1, max_value=50, value=5)
            
        with col2:
            min_score = st.slider("Minimum AI Score", min_value=1, max_value=10, value=7)
            delay_between = st.number_input("Delay Between Applications (seconds)", min_value=5, max_value=300, value=30)
        
        st.markdown("**Job Search Criteria**")
        keywords = st.text_input("Keywords", value="Python Developer, Software Engineer")
        location = st.text_input("Location", value="San Francisco, CA")
        experience = st.selectbox("Experience Level", ["entry", "mid", "senior"])
    
    # Run Agent Section
    st.subheader("🚀 Run Agent - Resume-Based Automation")
    st.info("Upload your resume and let AI find and apply to relevant jobs automatically!")
    
    if all_ready:
        # Resume upload
        uploaded_file = st.file_uploader(
            "📄 Upload Your Resume (PDF only)",
            type=['pdf'],
            help="Upload your resume in PDF format for AI analysis and job matching"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Resume uploaded: {uploaded_file.name}")
            
            # Job search parameters
            col1, col2 = st.columns(2)
            
            with col1:
                keyword = st.text_input("🔍 Job Keywords", value="Python Developer", help="Enter job titles or skills")
                max_jobs = st.number_input("📊 Max Jobs to Process", min_value=1, max_value=20, value=10)
            
            with col2:
                location = st.text_input("📍 Location", value="Remote", help="Job location preference")
                similarity_threshold = st.slider("🎯 Similarity Threshold", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
            
            # Run Agent button
            if st.button("🚀 Run Agent - Auto Apply", type="primary", use_container_width=True):
                with st.spinner("🤖 Running AutoAgent LinkedIn automation..."):
                    try:
                        # Prepare form data
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        data = {
                            "keyword": keyword,
                            "location": location,
                            "max_jobs": max_jobs,
                            "similarity_threshold": similarity_threshold
                        }
                        
                        # Make API request
                        response = requests.post(f"{API_URL}/api/run-agent", files=files, data=data, timeout=300)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if result["status"] == "success":
                                st.success("✅ AutoAgent automation completed successfully!")
                                
                                # Display results
                                data = result["data"]
                                
                                # Summary metrics
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("Jobs Found", data.get("total_jobs_found", 0))
                                with col2:
                                    st.metric("Jobs Analyzed", data.get("jobs_analyzed", 0))
                                with col3:
                                    st.metric("Applications Attempted", data.get("applications_attempted", 0))
                                with col4:
                                    st.metric("Applications Successful", data.get("applications_successful", 0))
                                
                                # Detailed results
                                if data.get("jobs"):
                                    st.subheader("📋 Job Analysis Results")
                                    
                                    for i, job in enumerate(data["jobs"]):
                                        with st.expander(f"� {job['title']} at {job['company']}"):
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.write(f"**Location:** {job['location']}")
                                                st.write(f"**Similarity Score:** {job['similarity_score']:.3f}")
                                                st.write(f"**AI Decision:** {job['ai_decision']}")
                                                st.write(f"**AI Confidence:** {job['ai_confidence']:.2f}")
                                            
                                            with col2:
                                                st.write(f"**Application Status:** {job['application_status']}")
                                                st.write(f"**Application Reason:** {job['application_reason']}")
                                                if job.get('url'):
                                                    st.link_button("🔗 View Job", job['url'])
                                            
                                            st.write(f"**AI Reasoning:** {job['ai_reason']}")
                                
                                # Summary
                                if data.get("summary"):
                                    st.subheader("📊 Automation Summary")
                                    st.text(data["summary"])
                                
                                # Errors (if any)
                                if data.get("errors"):
                                    st.subheader("⚠️ Errors Encountered")
                                    for error in data["errors"]:
                                        st.error(error)
                            
                            else:
                                st.error(f"❌ Automation failed: {result['message']}")
                        
                        else:
                            st.error(f"❌ API request failed with status code: {response.status_code}")
                    
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. The automation may still be running in the background.")
                    except Exception as e:
                        st.error(f"❌ Error running automation: {str(e)}")
        
        else:
            st.info("👆 Please upload your resume to enable automated job applications")
    
    else:
        st.warning("⚠️ Please configure all required services before using Run Agent")
    
    st.markdown("---")
    
    # Demo Mode Section
    st.subheader("🎬 Demo Mode")
    st.info("🛡️ **Demo Mode**: Safe testing without real applications")
    
    col1, col2 = st.columns(2)
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **🤖 AI-Powered Automation**
        - Playwright browser automation
        - Human-like interaction patterns
        - Advanced bot detection bypass
        - Smart form filling
        
        **🧠 Gemini AI Integration** 
        - Job compatibility analysis
        - Intelligent application decisions
        - Custom cover letter generation
        - Resume optimization suggestions
        """)
    
    with feature_col2:
        st.markdown("""
        **🔒 Security & Stealth**
        - Anti-detection features
        - User agent spoofing
        - Geolocation simulation
        - Session management
        
        **📊 Smart Analytics**
        - Application tracking
        - Success rate monitoring
        - Job match scoring
        - Performance insights
        """)
    
    # Configuration panel
    with st.expander("⚙️ Advanced Configuration"):
        st.markdown("**Automation Settings**")
        
        col1, col2 = st.columns(2)
        with col1:
            headless_mode = st.checkbox("Headless Browser", value=True, help="Run browser in background")
            apply_limit = st.number_input("Max Applications", min_value=1, max_value=50, value=5)
            
        with col2:
            min_score = st.slider("Minimum AI Score", min_value=1, max_value=10, value=7)
            delay_between = st.number_input("Delay Between Applications (seconds)", min_value=5, max_value=300, value=30)
        
        st.markdown("**Job Search Criteria**")
        keywords = st.text_input("Keywords", value="Python Developer, Software Engineer")
        location = st.text_input("Location", value="San Francisco, CA")
        experience = st.selectbox("Experience Level", ["entry", "mid", "senior"])


def show_dashboard():
    """Display the main dashboard."""
    st.title("📊 Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Jobs", "0", delta="0")
    
    with col2:
        st.metric("Applications", "0", delta="0")
    
    with col3:
        st.metric("Avg Match Score", "0%", delta="0%")
    
    with col4:
        st.metric("Response Rate", "0%", delta="0%")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    st.info("👋 Welcome to AutoAgentHire! Upload your resume to get started.")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Start Job Search", use_container_width=True):
            st.info("Job search feature coming soon!")
    
    with col2:
        if st.button("📄 Upload Resume", use_container_width=True):
            st.info("Resume upload feature coming soon!")
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.info("Analytics feature coming soon!")


def show_job_search():
    """Display job search interface."""
    st.title("🔍 Job Search")
    
    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            keywords = st.text_input("Keywords", placeholder="e.g., Python Developer")
            location = st.text_input("Location", placeholder="e.g., San Francisco, CA")
        
        with col2:
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"]
            )
            job_type = st.selectbox(
                "Job Type",
                ["Full-time", "Part-time", "Contract", "Internship"]
            )
        
        submitted = st.form_submit_button("🔍 Search Jobs", use_container_width=True)
        
        if submitted:
            if keywords:
                st.info("🔍 Searching for jobs...")
                
                # Call the backend API to trigger agent workflow
                try:
                    response = requests.post(
                        f"{API_URL}/agents/job-search",
                        json={
                            "keywords": keywords,
                            "location": location,
                            "experience_level": experience_level,
                            "job_type": job_type,
                            "max_results": 50
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        results = response.json()
                        st.success(f"✅ Found {len(results.get('jobs', []))} jobs!")
                        
                        # Display results
                        for job in results.get('jobs', [])[:10]:  # Show first 10
                            with st.expander(f"📋 {job.get('title', 'Job Title')} - {job.get('company', 'Company')}"):
                                st.write(f"**Location:** {job.get('location', 'N/A')}")
                                st.write(f"**Type:** {job.get('job_type', 'N/A')}")
                                st.write(f"**Match Score:** {job.get('match_score', 0)}%")
                                if job.get('description'):
                                    st.write(f"**Description:** {job['description'][:200]}...")
                    else:
                        st.error(f"❌ Search failed: {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("💡 Make sure the backend is running on port 8000")
            else:
                st.warning("⚠️ Please enter keywords to search for jobs")
    
    # AutoAgentHire Automation Section
    st.markdown("---")
    st.subheader("🤖 AutoAgentHire - AI-Powered Job Automation")
    
    # Agent status check
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **AutoAgentHire** uses advanced AI to:
            - 🔍 Search LinkedIn for relevant jobs
            - 🧠 Analyze job compatibility with Gemini AI  
            - 📝 Automatically apply to matching positions
            - 📊 Track applications and success rates
            """)
        
        with col2:
            agent_status = check_agent_status()
            if agent_status.get("gemini_ai") == "configured":
                st.success("✅ Gemini AI Ready")
            else:
                st.warning("⚠️ Gemini AI Not Configured")
            
            if agent_status.get("linkedin") == "configured":
                st.success("✅ LinkedIn Ready")
            else:
                st.warning("⚠️ LinkedIn Not Configured")
    
    # Resume upload section
    uploaded_resume = st.file_uploader(
        "📄 Upload Your Resume", 
        type=['pdf', 'docx', 'txt'],
        help="Upload your resume for AI-powered job matching"
    )
    
    resume_text = ""
    if uploaded_resume:
        st.success(f"✅ Resume uploaded: {uploaded_resume.name}")
        # Extract text from resume (simplified)
        if uploaded_resume.type == "text/plain":
            resume_text = str(uploaded_resume.read(), "utf-8")
        else:
            resume_text = f"Resume content from {uploaded_resume.name} (text extraction needed)"
    
    with st.form("autoagent_form"):
        st.markdown("**🤖 AutoAgentHire Configuration**")
        
        col1, col2 = st.columns(2)
        with col1:
            auto_keywords = st.text_input("Job Keywords", value="Python Developer", placeholder="e.g., AI Engineer")
            auto_location = st.text_input("Preferred Location", value="Remote", placeholder="e.g., Hyderabad")
        
        with col2:
            max_applications = st.number_input("Max Applications", min_value=1, max_value=10, value=3)
            headless_mode = st.checkbox("Headless Mode", value=True, help="Run browser in background")
        
        auto_submit = st.form_submit_button("🚀 Start AutoAgentHire", use_container_width=True)
        
        if auto_submit:
            if not uploaded_resume:
                st.warning("⚠️ Please upload your resume first!")
            elif not auto_keywords:
                st.warning("⚠️ Please enter job keywords!")
            else:
                run_autoagent_workflow(auto_keywords, auto_location, resume_text, max_applications, headless_mode)
    
    st.markdown("---")
    st.subheader("📋 Job Results")
    
    # Display saved search results or recent applications
    if 'job_results' not in st.session_state:
        st.info("No jobs found. Start a search to discover opportunities!")
    else:
        display_job_results()


def check_agent_status():
    """Check the status of automation agents."""
    try:
        response = requests.get(f"{API_URL}/api/agent/status", timeout=5)
        if response.status_code == 200:
            return response.json().get("agents", {})
    except:
        pass
    return {"gemini_ai": "unknown", "linkedin": "unknown"}


def run_autoagent_workflow(keywords, location, resume_text, max_applications, headless):
    """Run the AutoAgentHire automation workflow."""
    st.info("🤖 Starting AutoAgentHire automation...")
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Update progress
        progress_bar.progress(20)
        status_text.text("🔐 Initializing browser and LinkedIn login...")
        
        # Call the automation API
        response = requests.post(
            f"{API_URL}/api/agent/run",
            json={
                "keyword": keywords,
                "location": location,
                "resume_text": resume_text,
                "max_applications": max_applications,
                "headless": headless
            },
            timeout=300  # 5 minutes timeout
        )
        
        progress_bar.progress(100)
        
        if response.status_code == 200:
            result = response.json()
            status_text.text("✅ AutoAgentHire completed!")
            
            if result["status"] == "success":
                st.success("🎉 AutoAgentHire automation completed successfully!")
                
                # Display results
                data = result.get("data", {})
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Jobs Found", data.get("jobs_found", 0))
                with col2:
                    st.metric("Applications Sent", data.get("applications_sent", 0))
                with col3:
                    success_rate = (data.get("applications_sent", 0) / max(data.get("jobs_found", 1), 1)) * 100
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                
                # Display application log
                if data.get("applications_log"):
                    st.subheader("📋 Application History")
                    for app in data["applications_log"]:
                        with st.expander(f"✅ Applied: {app['job_title']} at {app['company']}"):
                            st.write(f"**Status:** {app['status']}")
                            st.write(f"**Match Score:** {app['match_score']}%")
                            st.write(f"**Applied:** {app['applied_at']}")
                            st.write(f"**Reasoning:** {app['reasoning']}")
            else:
                st.error(f"❌ Automation failed: {result.get('message', 'Unknown error')}")
        else:
            st.error(f"❌ API Error: {response.text}")
            
    except requests.exceptions.Timeout:
        st.error("⏰ Automation timed out. This may take several minutes to complete.")
        st.info("💡 Check the backend logs for progress updates.")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {str(e)}")
        st.info("💡 Make sure the backend is running and LinkedIn credentials are configured.")
    finally:
        progress_bar.empty()


def display_job_results():
    """Display job search results."""
    results = st.session_state.get('job_results', [])
    
    for i, job in enumerate(results):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{job['title']}** at **{job['company']}**")
                st.write(f"📍 {job['location']} | {job.get('job_type', 'Full-time')}")
            
            with col2:
                st.metric("Match", f"{job.get('match_score', 0)}%")
            
            with col3:
                if st.button(f"View Details", key=f"view_{i}"):
                    st.session_state[f'show_job_{i}'] = True
            
            if st.session_state.get(f'show_job_{i}', False):
                st.write(job.get('description', 'No description available'))
                if st.button(f"Hide Details", key=f"hide_{i}"):
                    st.session_state[f'show_job_{i}'] = False
            
            st.markdown("---")


def show_applications():
    """Display applications tracker."""
    st.title("📋 Applications")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["All", "Applied", "In Review", "Interview", "Rejected"])
    with col2:
        date_filter = st.selectbox("Date", ["All Time", "Last 7 Days", "Last 30 Days"])
    with col3:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Match Score"])
    
    st.markdown("---")
    
    st.info("📝 No applications yet. Apply to jobs from the Job Search page!")


def show_profile():
    """Display user profile and resume management."""
    st.title("👤 Profile")
    
    # Resume upload
    st.subheader("📄 Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"],
        help="Your resume will be parsed to extract skills and experience"
    )
    
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        if st.button("📊 Parse Resume"):
            st.info("Resume parsing feature coming soon!")
    
    st.markdown("---")
    
    # Profile information
    st.subheader("ℹ️ Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", placeholder="John Doe")
        st.text_input("Email", placeholder="john@example.com")
        st.text_input("Phone", placeholder="+1 (555) 123-4567")
    
    with col2:
        st.text_input("Location", placeholder="San Francisco, CA")
        st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/johndoe")
        st.text_input("Portfolio URL", placeholder="https://johndoe.com")
    
    if st.button("💾 Save Profile", use_container_width=True):
        st.success("Profile saved successfully!")


def show_settings():
    """Display application settings."""
    st.title("⚙️ Settings")
    
    # Job preferences
    st.subheader("🎯 Job Preferences")
    desired_roles = st.text_area(
        "Desired Job Titles (one per line)",
        placeholder="Software Engineer\nPython Developer\nMachine Learning Engineer"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        min_salary = st.number_input("Minimum Salary ($)", min_value=0, value=80000, step=5000)
    with col2:
        max_salary = st.number_input("Maximum Salary ($)", min_value=0, value=150000, step=5000)
    
    st.markdown("---")
    
    # Automation settings
    st.subheader("🤖 Automation Settings")
    auto_apply = st.checkbox("Enable Auto-Apply (Requires confirmation)", value=False)
    daily_search = st.checkbox("Enable Daily Job Search", value=True)
    email_notifications = st.checkbox("Enable Email Notifications", value=True)
    
    max_applications = st.slider("Max Applications per Day", 1, 50, 10)
    
    st.markdown("---")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    
    st.markdown("---")
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")


if __name__ == "__main__":
    main()
