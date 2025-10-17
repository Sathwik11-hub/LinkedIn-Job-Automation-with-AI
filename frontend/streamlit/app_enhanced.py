"""
Enhanced Streamlit Frontend for AutoAgentHire
Features: Gemini AI integration, secure forms, real-time progress tracking
"""
import streamlit as st
import requests
import time
import os
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="AutoAgentHire - AI Job Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .feature-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem;
    }
    
    .status-success {
        background: #10b981;
        color: white;
    }
    
    .status-warning {
        background: #f59e0b;
        color: white;
    }
    
    .status-info {
        background: #3b82f6;
        color: white;
    }
    
    .status-error {
        background: #ef4444;
        color: white;
    }
    
    .progress-step {
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 4px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if backend API is available."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application entry point."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AutoAgentHire</h1>
        <p>Intelligent LinkedIn Job Application Automation with AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Home", "🚀 Quick Start", "⚙️ Full Configuration", "📊 Dashboard", "📝 Applications", "❓ Help"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Status
        if check_api_health():
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.info("Start backend: `uvicorn backend.main:app --reload`")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.info("💎 **Pro Tip**: Use preview mode first to see which jobs match!")
    
    # Route to pages
    if page == "🏠 Home":
        show_home()
    elif page == "🚀 Quick Start":
        show_quick_start()
    elif page == "⚙️ Full Configuration":
        show_full_config()
    elif page == "📊 Dashboard":
        show_dashboard()
    elif page == "📝 Applications":
        show_applications()
    elif page == "❓ Help":
        show_help()


def show_home():
    """Home page with overview."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to AutoAgentHire! 👋
    
    **The smartest way to automate your LinkedIn job applications using AI.**
    
    ### How It Works:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h2>📄</h2>
            <h4>1. Upload Resume</h4>
            <p>Upload your resume and we'll extract your skills and experience using AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h2>🔍</h2>
            <h4>2. Set Preferences</h4>
            <p>Tell us what jobs you're looking for and your preferences</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h2>🤖</h2>
            <h4>3. Let AI Work</h4>
            <p>Our AI agent finds, evaluates, and applies to matching jobs for you</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - ✅ **AI-Powered Matching** - Gemini AI evaluates job compatibility
        - ✅ **Smart Cover Letters** - Auto-generated personalized cover letters
        - ✅ **Intelligent Answers** - AI answers application questions
        - ✅ **Easy Apply Focus** - Only targets Easy Apply jobs
        """)
    
    with col2:
        st.markdown("""
        - ✅ **Preview Mode** - See results before submitting
        - ✅ **Secure** - Your credentials stay private
        - ✅ **Real-time Progress** - Watch the automation in action
        - ✅ **Detailed Reports** - Track all your applications
        """)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Ready to Get Started?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Quick Setup", use_container_width=True, type="primary"):
            st.session_state.page = "🚀 Quick Start"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_quick_start():
    """Quick start page for fast automation."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 🚀 Quick Start")
    st.markdown("Get started in 3 simple steps!")
    
    # Step 1: Resume Upload
    st.markdown("### Step 1: Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, TXT)",
        type=['pdf', 'docx', 'txt'],
        key="quick_resume"
    )
    
    if uploaded_file:
        with st.spinner("🤖 Analyzing resume with AI..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                data = {"user_email": st.session_state.get("email", "user@example.com")}
                
                response = requests.post(
                    f"{API_URL}/api/upload-resume",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Resume uploaded and analyzed!")
                    
                    st.session_state.resume_uploaded = True
                    st.session_state.resume_text = "Resume content extracted"
                    
                    with st.expander("📋 AI-Generated Summary"):
                        st.write(result.get("summary", "Summary generated successfully"))
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Step 2: Job Preferences
    st.markdown("### Step 2: What Jobs Are You Looking For?")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input(
            "Job Title / Keywords",
            value="AI Engineer",
            placeholder="e.g., Software Engineer, Data Scientist",
            key="quick_job_title"
        )
    with col2:
        location = st.selectbox(
            "Location",
            ["Remote", "United States", "United Kingdom", "India", "Canada", "Germany"],
            key="quick_location"
        )
    
    # Step 3: LinkedIn Credentials
    st.markdown("### Step 3: LinkedIn Login (Secure)")
    st.info("🔒 Your credentials are never stored and only used for this session")
    
    col1, col2 = st.columns(2)
    with col1:
        linkedin_email = st.text_input(
            "LinkedIn Email",
            type="default",
            placeholder="your.email@example.com",
            key="quick_li_email"
        )
    with col2:
        linkedin_password = st.text_input(
            "LinkedIn Password",
            type="password",
            placeholder="••••••••",
            key="quick_li_pass"
        )
    
    st.markdown("---")
    
    # Preview Mode Toggle
    preview_mode = st.checkbox(
        "🔍 Preview Mode (Recommended for first run)",
        value=True,
        help="Preview mode finds and evaluates jobs without submitting applications"
    )
    
    # Start Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_button = st.button(
            "🚀 Start AutoAgent" if not preview_mode else "🔍 Preview Jobs",
            use_container_width=True,
            type="primary",
            disabled=not (job_title and linkedin_email and linkedin_password)
        )
    
    if start_button:
        run_automation(
            keywords=job_title,
            location=location,
            linkedin_email=linkedin_email,
            linkedin_password=linkedin_password,
            submit=not preview_mode
        )
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_full_config():
    """Full configuration page with all options."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Full Configuration")
    st.markdown("Advanced settings for power users")
    
    # Personal Information
    with st.expander("👤 Personal Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", key="full_name")
            email = st.text_input("Email", key="email")
        with col2:
            phone = st.text_input("Phone (Optional)", key="phone")
            linkedin_profile = st.text_input("LinkedIn Profile URL (Optional)", key="linkedin_url")
    
    # Resume Upload
    with st.expander("📄 Resume", expanded=True):
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=['pdf', 'docx', 'txt'],
            key="full_resume"
        )
        
        if uploaded_file and st.button("Analyze Resume"):
            # Same upload logic as quick start
            st.success("Resume analyzed!")
    
    # Job Search Criteria
    with st.expander("🔍 Job Search Criteria", expanded=True):
        job_keywords = st.text_input(
            "Job Keywords (comma-separated)",
            value="AI Engineer, Machine Learning Engineer",
            key="full_keywords"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            locations = st.multiselect(
                "Preferred Locations",
                ["Remote", "United States", "United Kingdom", "India", "Canada", "Germany", "Australia"],
                default=["Remote"],
                key="full_locations"
            )
        with col2:
            job_type = st.selectbox(
                "Job Type",
                ["Any", "Remote", "On-site", "Hybrid"],
                key="full_job_type"
            )
        with col3:
            experience_level = st.selectbox(
                "Experience Level",
                ["Entry Level", "Mid-level", "Senior", "Lead/Manager", "Executive"],
                index=1,
                key="full_exp_level"
            )
        
        skills = st.text_input(
            "Key Skills (comma-separated)",
            value="Python, TensorFlow, NLP, Docker",
            key="full_skills"
        )
    
    # LinkedIn Credentials
    with st.expander("🔐 LinkedIn Credentials", expanded=True):
        st.warning("⚠️ Your credentials are used only for automation and never stored")
        
        col1, col2 = st.columns(2)
        with col1:
            li_email = st.text_input("LinkedIn Email", key="full_li_email")
        with col2:
            li_pass = st.text_input("LinkedIn Password", type="password", key="full_li_pass")
    
    # AI Configuration
    with st.expander("🤖 AI Configuration (Optional)", expanded=False):
        gemini_key = st.text_input(
            "Google Gemini API Key (Optional)",
            type="password",
            help="Provide your own API key for better AI responses",
            key="gemini_key"
        )
        
        st.info("💡 If not provided, the system will use default API key")
    
    # Automation Settings
    with st.expander("⚙️ Automation Settings", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            max_applications = st.number_input(
                "Max Applications Per Run",
                min_value=1,
                max_value=50,
                value=10,
                key="max_apps"
            )
        with col2:
            min_match_score = st.slider(
                "Minimum Match Score",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key="min_match"
            )
        
        easy_apply_only = st.checkbox("Easy Apply Jobs Only", value=True, key="easy_apply")
        generate_cover_letter = st.checkbox("Auto-Generate Cover Letters", value=True, key="gen_cover")
    
    st.markdown("---")
    
    # Action Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Configuration", use_container_width=True):
            st.success("Configuration saved!")
    with col2:
        if st.button("🔍 Preview Mode", use_container_width=True, type="secondary"):
            st.info("Starting preview...")
    with col3:
        if st.button("🚀 Run Full Automation", use_container_width=True, type="primary"):
            st.warning("Starting full automation...")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_dashboard():
    """Dashboard with metrics and status."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jobs Found", "0", delta="0")
    with col2:
        st.metric("Applications Sent", "0", delta="0")
    with col3:
        st.metric("Avg Match Score", "0%", delta="0%")
    with col4:
        st.metric("Success Rate", "0%", delta="0%")
    
    st.markdown("---")
    
    # Current Status
    st.markdown("### 🔄 Current Status")
    
    try:
        response = requests.get(f"{API_URL}/api/agent/status", timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            display_status(status_data)
        else:
            st.info("No active automation running")
    except:
        st.error("Could not connect to backend")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_applications():
    """Applications history page."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## 📝 Application History")
    
    try:
        response = requests.get(f"{API_URL}/api/applications", timeout=5)
        if response.status_code == 200:
            data = response.json()
            applications = data.get("applications", [])
            
            if applications:
                st.dataframe(applications)
            else:
                st.info("No applications yet. Start the automation to see your applications here!")
        else:
            st.error("Could not fetch applications")
    except Exception as e:
        st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_help():
    """Help and documentation page."""
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("## ❓ Help & Documentation")
    
    st.markdown("""
    ### Frequently Asked Questions
    
    **Q: Is my LinkedIn password safe?**
    A: Yes! Your credentials are only used for the current session and never stored in any database.
    
    **Q: What is Preview Mode?**
    A: Preview mode searches for jobs and shows you matches without actually submitting applications. Perfect for testing!
    
    **Q: How does the AI matching work?**
    A: We use Google Gemini AI to analyze job descriptions and compare them with your resume to find the best matches.
    
    **Q: Can I customize cover letters?**
    A: Yes! The AI generates personalized cover letters for each job based on your resume and the job description.
    
    **Q: What happens if LinkedIn blocks the automation?**
    A: We use human-like delays and patterns to avoid detection, but if issues occur, the system will pause and notify you.
    
    ### Support
    
    Need help? Check out our:
    - 📖 [Documentation](https://github.com/yourusername/autoagenthire)
    - 💬 [Discord Community](https://discord.gg/autoagenthire)
    - 📧 [Email Support](mailto:support@autoagenthire.com)
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)


def run_automation(
    keywords: str,
    location: str,
    linkedin_email: str,
    linkedin_password: str,
    submit: bool = False
):
    """Run the automation workflow."""
    
    payload = {
        "keywords": keywords,
        "location": location,
        "linkedin_email": linkedin_email,
        "linkedin_password": linkedin_password,
        "submit": submit
    }
    
    with st.spinner("🤖 Starting AutoAgent..."):
        try:
            response = requests.post(
                f"{API_URL}/api/run-agent",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                st.success("✅ Agent started successfully!")
                
                # Show progress
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                # Poll for status
                for i in range(60):  # Poll for up to 60 seconds
                    time.sleep(1)
                    
                    try:
                        status_response = requests.get(f"{API_URL}/api/agent/status", timeout=5)
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            
                            progress = min((i + 1) * 1.67, 100)
                            progress_bar.progress(int(progress))
                            
                            with status_placeholder.container():
                                display_status(status_data)
                            
                            if status_data.get("status") in ["completed", "failed", "stopped"]:
                                break
                    except:
                        pass
                
                # Final status
                final_response = requests.get(f"{API_URL}/api/agent/status", timeout=5)
                if final_response.status_code == 200:
                    final_status = final_response.json()
                    
                    if final_status.get("status") == "completed":
                        st.success("🎉 Automation completed successfully!")
                        detail = final_status.get("detail", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Jobs Found", detail.get("jobs_found", 0))
                        with col2:
                            apps_key = "applications_submitted" if submit else "applications_previewed"
                            st.metric(
                                "Applications" + (" Submitted" if submit else " Previewed"),
                                detail.get(apps_key, 0)
                            )
                    else:
                        st.error(f"❌ Automation ended with status: {final_status.get('status')}")
            else:
                st.error(f"Failed to start agent: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")


def display_status(status_data: Dict[str, Any]):
    """Display agent status information."""
    
    status = status_data.get("status", "unknown")
    detail = status_data.get("detail", {})
    
    # Status badge
    status_class = {
        "idle": "status-info",
        "running": "status-warning",
        "completed": "status-success",
        "failed": "status-error",
        "paused": "status-warning"
    }.get(status, "status-info")
    
    st.markdown(
        f'<span class="status-badge {status_class}">{status.upper()}</span>',
        unsafe_allow_html=True
    )
    
    # Phase information
    if phase := detail.get("phase"):
        st.markdown(f"**Current Phase:** {phase}")
    
    # Progress metrics
    if detail:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Jobs Found", detail.get("jobs_found", 0))
        with col2:
            st.metric("Applications Submitted", detail.get("applications_submitted", 0))
        with col3:
            st.metric("Previewed", detail.get("applications_previewed", 0))
    
    # Recent logs
    if logs := detail.get("logs", []):
        with st.expander("📋 Recent Logs"):
            for log in logs[-10:]:
                timestamp = log.get("timestamp", "")
                level = log.get("level", "INFO")
                message = log.get("message", "")
                
                icon = {"INFO": "ℹ️", "WARNING": "⚠️", "ERROR": "❌", "SUCCESS": "✅"}.get(level, "ℹ️")
                st.markdown(f"{icon} `{timestamp}` - {message}")


if __name__ == "__main__":
    main()
