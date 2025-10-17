"""
Streamlit frontend application for AutoAgentHire.
Provides a user-friendly dashboard for job search automation.
"""
import streamlit as st
import requests
from typing import Optional

# Page config
st.set_page_config(
    page_title="AutoAgentHire",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_URL = "http://localhost:8000"


def check_api_health() -> bool:
    """Check if the backend API is available."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application function."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 AutoAgentHire")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "🔍 Job Search", "📋 Applications", "👤 Profile", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.info("Start the backend: `uvicorn backend.main:app --reload`")
    
    # Main content
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🔍 Job Search":
        show_job_search()
    elif page == "📋 Applications":
        show_applications()
    elif page == "👤 Profile":
        show_profile()
    elif page == "⚙️ Settings":
        show_settings()


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
            st.info("🔍 Searching for jobs... (Feature in development)")
    
    st.markdown("---")
    st.subheader("📋 Job Results")
    st.info("No jobs found. Start a search to discover opportunities!")


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
