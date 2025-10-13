"""
Enhanced AutoAgentHire Frontend
Beautiful, modern UI with improved UX for LinkedIn job automation.
"""
import streamlit as st
import requests
import time
import json
from typing import Optional

# Backend configuration
BACKEND_URL = "http://127.0.0.1:8000"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"
JOB_SEARCH_ENDPOINT = f"{BACKEND_URL}/agents/job-search"

# Page config with custom theme
st.set_page_config(
    page_title="AutoAgentHire - AI Job Automation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Custom card styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    h1 {
        color: white;
        font-weight: 700;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    h2 {
        color: rgba(255,255,255,0.9);
        font-weight: 500;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    h3 {
        color: white;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Card container */
    .card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed #667eea;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f5f7fa;
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background-color: transparent;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Checkbox */
    .stCheckbox > label {
        font-weight: 500;
        color: #333;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    /* Status indicators */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-success {
        background: #10b981;
        color: white;
    }
    
    .status-error {
        background: #ef4444;
        color: white;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Icon styling */
    .icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
# Backend configuration
BACKEND_URL = "http://127.0.0.1:8000"
HEALTH_ENDPOINT = f"{BACKEND_URL}/health"
JOB_SEARCH_ENDPOINT = f"{BACKEND_URL}/agents/job-search"
AUTOAGENT_ENDPOINT = f"{BACKEND_URL}/api/run-agent"
AUTOAGENT_FILE_ENDPOINT = f"{BACKEND_URL}/api/run-agent-with-file"
AGENT_STATUS_ENDPOINT = f"{BACKEND_URL}/api/agent/status"

def check_api_health():
    """Check if the backend API is available."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_agent_status():
    """Get agent status from backend."""
    try:
        response = requests.get(AGENT_STATUS_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def run_automation(file, job_preferences):
    """Run the AutoAgent automation."""
    try:
        # Handle case where no file is uploaded (Quick Start mode)
        if file is not None:
            # When uploading a resume, use the file endpoint and send expected form fields
            files = {"file": (file.name, file.getvalue(), "application/pdf")}
            form_data = {
                "keyword": job_preferences.get("keyword", job_preferences.get("job_title", "AI Engineer")),
                "location": job_preferences.get("location", "Remote"),
                "max_jobs": job_preferences.get("max_jobs", 10),
                "similarity_threshold": job_preferences.get("similarity_threshold", 0.6)
            }

            response = requests.post(
                AUTOAGENT_FILE_ENDPOINT,
                files=files,
                data=form_data,
                timeout=300
            )
        else:
            # For Quick Start mode, just send preferences without file
            data = {"preferences": job_preferences}
            response = requests.post(
                AUTOAGENT_ENDPOINT,
                json=data,
                timeout=300
            )
        
        return response.json() if response.status_code == 200 else None
        
    except Exception as e:
        st.error(f"Error running automation: {str(e)}")
        return None

def main():
    # Header with gradient background
    st.markdown('<h1>🤖 AutoAgentHire</h1>', unsafe_allow_html=True)
    st.markdown('<h2>AI-Powered LinkedIn Job Automation</h2>', unsafe_allow_html=True)
    
    # API Status Banner
    api_status = check_api_health()
    if not api_status:
        st.error("🔌 Backend API is not running. Please start the backend server first.")
        with st.expander("📖 How to start the backend"):
            st.code("""
# Start the backend server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 50501
            """)
        return
    
    # System Status Indicator
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="status-badge status-success">✅ API Connected</div>', unsafe_allow_html=True)
        with col2:
            agent_status = get_agent_status()
            if agent_status and agent_status.get("agents", {}).get("gemini_ai") == "configured":
                st.markdown('<div class="status-badge status-success">🤖 AI Ready</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-badge status-error">⚠️ AI Not Configured</div>', unsafe_allow_html=True)
        with col3:
            if agent_status and agent_status.get("agents", {}).get("linkedin") == "configured":
                st.markdown('<div class="status-badge status-success">💼 LinkedIn Ready</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-badge status-error">⚠️ LinkedIn Not Configured</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Start AutoAgent Section
    st.markdown("### 🚀 Quick Start AutoAgent")
    st.markdown("Start LinkedIn job automation with default settings or customize your preferences below.")
    
    quick_col1, quick_col2, quick_col3 = st.columns([2, 2, 1])
    
    with quick_col1:
        quick_job_title = st.text_input("Job Title", value="AI Engineer", key="quick_job")
    
    with quick_col2:
        quick_location = st.selectbox("Location", ["Remote", "United States", "India", "Canada"], key="quick_location")
    
    with quick_col3:
        quick_run_button = st.button(
            "🚀 Start AutoAgent",
            type="primary",
            use_container_width=True,
            help="Start LinkedIn job automation with current settings"
        )
    
    if quick_run_button:
        # Quick start automation
        st.info("🤖 Starting AutoAgent with quick settings...")
        
        quick_preferences = {
            "job_title": quick_job_title,
            "location": quick_location,
            "experience_level": "mid",
            "resume_path": "data/resumes/default_resume.txt"
        }
        
        with st.spinner("🔄 Running AutoAgent automation..."):
            result = run_automation(None, quick_preferences)
            
            if result and result.get("status") == "success":
                job_id = result.get("job_id")
                st.success("✅ AutoAgent job queued successfully!")
                if job_id:
                    st.info(f"Job queued with id: {job_id}. Poll /api/agent/status to track progress.")
            
                
                # Show basic results
                if "execution_summary" in result:
                    exec_summary = result["execution_summary"]
                    
                    summary_col1, summary_col2, summary_col3 = st.columns(3)
                    with summary_col1:
                        st.metric("Jobs Found", exec_summary.get("total_jobs_found", 0))
                    with summary_col2:
                        st.metric("Applications Submitted", exec_summary.get("applications_submitted", 0))
                    with summary_col3:
                        st.metric("Success Rate", f"{exec_summary.get('success_rate', 0)}%")
            else:
                st.error("❌ AutoAgent automation failed. Please check your configuration.")
    
    st.markdown("---")
    st.markdown("### ⚙️ Advanced Configuration")
    st.markdown("For detailed customization, use the options below:")
    
    st.markdown("---")
    
    # Main content in two columns
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown("### 📄 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Drop your resume here or click to browse",
            type=['pdf'],
            help="Upload your resume in PDF format for AI-powered job matching",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            st.success(f"✅ Resume uploaded: **{uploaded_file.name}**")
            file_size_kb = len(uploaded_file.getvalue()) / 1024
            st.info(f"📊 File size: {file_size_kb:.2f} KB")
            
            # Resume preview section
            with st.expander("👁️ Resume Info"):
                st.write(f"**Filename:** {uploaded_file.name}")
                st.write(f"**Type:** {uploaded_file.type}")
                st.write(f"**Size:** {file_size_kb:.2f} KB")
    
    with col_right:
        st.markdown("### ⚙️ Job Search Preferences")
        
        # Tabbed interface for preferences
        tab1, tab2, tab3 = st.tabs(["🔍 Basic Search", "💼 Job Details", "🎯 Advanced"])
        
        with tab1:
            keyword = st.text_input(
                "Job Role/Keyword",
                value="AI Engineer",
                placeholder="e.g., Python Developer, Data Scientist",
                help="Enter the job title or keywords you're looking for"
            )
            
            location_options = [
                "Remote", "India", "United States", "United Kingdom", 
                "Canada", "Germany", "Singapore", "Australia", "Custom"
            ]
            location = st.selectbox(
                "Location Preference",
                options=location_options,
                index=0,
                help="Select your preferred job location"
            )
            
            if location == "Custom":
                location = st.text_input("Enter Custom Location", placeholder="e.g., New York, NY")
            
            skills = st.text_area(
                "Key Skills",
                value="Python, Machine Learning, AI, Data Science",
                placeholder="List your key skills separated by commas",
                help="Enter your main skills for better job matching",
                height=100
            )
        
        with tab2:
            experience_level = st.selectbox(
                "Experience Level",
                options=["Any", "Entry Level", "Associate", "Mid-Senior Level", "Director", "Executive"],
                index=0,
                help="Select your experience level"
            )
            
            job_type = st.selectbox(
                "Job Type",
                options=["Any", "Full-time", "Part-time", "Contract", "Temporary", "Internship"],
                index=1,
                help="Select preferred job type"
            )
            
            salary_options = [
                "Any", "$40,000+", "$60,000+", "$80,000+", 
                "$100,000+", "$120,000+", "$150,000+"
            ]
            salary_range = st.selectbox(
                "Salary Range (Annual)",
                options=salary_options,
                index=0,
                help="Select minimum salary expectation"
            )
        
        with tab3:
            max_jobs = st.slider(
                "Maximum Jobs to Process",
                min_value=1,
                max_value=50,
                value=15,
                help="Number of jobs to analyze and potentially apply to"
            )
            
            similarity_threshold = st.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.6,
                step=0.1,
                help="Minimum similarity score to apply (higher = more selective)"
            )
            
            auto_apply = st.checkbox(
                "🚀 Enable Automatic Applications",
                value=True,
                help="Automatically apply to jobs that meet your criteria"
            )
            
            if not auto_apply:
                st.warning("⚠️ Auto-apply disabled. Jobs will be analyzed only.")
    
    # Preferences summary
    job_preferences = {
        "keyword": keyword,
        "location": location,
        "skills": skills,
        "experience_level": experience_level,
        "job_type": job_type,
        "salary_range": salary_range,
        "max_jobs": max_jobs,
        "similarity_threshold": similarity_threshold,
        "auto_apply": auto_apply
    }
    
    st.markdown("---")
    
    # Preferences Summary Card
    if uploaded_file and keyword:
        with st.expander("📋 Current Job Preferences Summary", expanded=False):
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.markdown("**Search Criteria**")
                st.write(f"🎯 Role: {keyword}")
                st.write(f"📍 Location: {location}")
                st.write(f"📊 Max Jobs: {max_jobs}")
            
            with summary_col2:
                st.markdown("**Job Requirements**")
                st.write(f"💼 Type: {job_type}")
                st.write(f"💰 Salary: {salary_range}")
                st.write(f"📈 Experience: {experience_level}")
            
            with summary_col3:
                st.markdown("**Settings**")
                st.write(f"🎯 Threshold: {similarity_threshold}")
                st.write(f"🤖 Auto Apply: {'✅ Yes' if auto_apply else '❌ No'}")
                st.write(f"🛠️ Skills: {len(skills.split(','))} listed")
        
        # Run Automation Button
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            run_button = st.button(
                "🚀 Run AutoAgent Automation",
                type="primary",
                use_container_width=True
            )
        
        if run_button:
            # Progress indicator
            with st.spinner("🤖 Initializing AI automation..."):
                time.sleep(1)  # Simulated delay for UX
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 20:
                    status_text.text("🔐 Logging into LinkedIn...")
                elif i < 40:
                    status_text.text("🔍 Searching for jobs...")
                elif i < 70:
                    status_text.text("🤖 Analyzing job compatibility...")
                else:
                    status_text.text("📝 Processing applications...")
                time.sleep(0.02)
            
            # Run actual automation
            result = run_automation(uploaded_file, job_preferences)
            
            progress_bar.empty()
            status_text.empty()
            
            if result and result.get("status") == "success":
                job_id = result.get("job_id")
                st.success("✅ AutoAgent job queued successfully!")
                if job_id:
                    st.info(f"Job queued with id: {job_id}. Poll /api/agent/status to track progress.")
                
                data = result.get("data", {})
                
                # Results metrics
                st.markdown("### 📊 Automation Results")
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric(
                        "Jobs Found",
                        data.get("jobs_found", 0),
                        delta=None
                    )
                
                with metric_col2:
                    st.metric(
                        "Jobs Analyzed",
                        data.get("jobs_analyzed", 0),
                        delta=None
                    )
                
                with metric_col3:
                    st.metric(
                        "Applications Attempted",
                        data.get("applications_attempted", 0),
                        delta=None
                    )
                
                with metric_col4:
                    success_rate = 0
                    if data.get("applications_attempted", 0) > 0:
                        success_rate = (data.get("successful_applications", 0) / 
                                      data.get("applications_attempted", 1)) * 100
                    st.metric(
                        "Success Rate",
                        f"{success_rate:.0f}%",
                        delta=None
                    )
                
                # Detailed job results
                if data.get("jobs"):
                    st.markdown("### � Job Analysis Details")
                    
                    for i, job in enumerate(data["jobs"], 1):
                        with st.expander(f"Job {i}: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}"):
                            job_col1, job_col2 = st.columns([2, 1])
                            
                            with job_col1:
                                st.markdown("**Job Information**")
                                st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
                                
                                if job.get('url'):
                                    st.markdown(f"[🔗 View Job Posting]({job['url']})")
                                
                                analysis = job.get('analysis', {})
                                if analysis:
                                    st.markdown("**AI Analysis**")
                                    similarity = analysis.get('similarity_score', 0)
                                    st.progress(similarity / 100)
                                    st.write(f"Similarity Score: **{similarity}%**")
                                    
                                    if analysis.get('analysis'):
                                        st.info(f"💡 {analysis['analysis']}")
                            
                            with job_col2:
                                if job.get('applied'):
                                    st.success("✅ Application Submitted")
                                else:
                                    st.info("ℹ️ Not Applied")
                                
                                if job.get('application_date'):
                                    st.write(f"📅 {job['application_date']}")
                
                # Errors section
                if data.get("errors"):
                    st.markdown("### ⚠️ Issues Encountered")
                    for error in data["errors"]:
                        st.warning(error)
            
            elif result:
                st.error(f"❌ Automation failed: {result.get('message', 'Unknown error')}")
            else:
                st.error("❌ Failed to run automation. Please check backend logs.")
    
    else:
        # Call to action
        st.info("📌 **Get Started:** Upload your resume and configure job preferences to begin automated job hunting!")
    
    # Footer with features
    st.markdown("---")
    st.markdown("### 🎯 How AutoAgentHire Works")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">📄</div>
            <h4>1. Upload Resume</h4>
            <p>Upload your PDF resume for AI-powered analysis and skill extraction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🤖</div>
            <h4>2. AI Analysis</h4>
            <p>Gemini AI analyzes job compatibility and makes intelligent decisions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div class="feature-card">
            <div class="icon">🚀</div>
            <h4>3. Auto Apply</h4>
            <p>Automated applications to matching positions on LinkedIn</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional info
    with st.expander("ℹ️ About AutoAgentHire"):
        st.markdown("""
        **AutoAgentHire** is an advanced AI-powered job automation platform that:
        
        - 🌐 Opens LinkedIn in a Chromium browser
        - 🔐 Securely logs in with your credentials
        - 🔍 Searches for relevant job opportunities
        - 🤖 Uses Gemini AI to analyze job compatibility
        - 📝 Automatically applies to matching positions
        - 📊 Provides detailed analytics and insights
        
        **Privacy & Security:**
        - All automation runs locally on your machine
        - Your credentials are stored securely in environment variables
        - No data is shared with third parties
        
        **Note:** The automation runs in a visible browser window so you can monitor the entire process.
        """)

if __name__ == "__main__":
    main()