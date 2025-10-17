"""
Streamlit frontend application for AutoAgentHire.
Beautiful UI with gradient backgrounds and glass morphism effects.
"""
import streamlit as st
import requests
import time
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

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #9333ea 0%, #2563eb 100%);
        background-attachment: fixed;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-active {
        background: #10b981;
        color: white;
    }
    
    .status-pending {
        background: #3b82f6;
        color: white;
    }
    
    .status-paused {
        background: #f59e0b;
        color: white;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #9333ea 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(147, 51, 234, 0.5);
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if the backend API is available."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application function."""
    
    # Hero section
    st.markdown("""
    <div style="text-align:center;padding:2rem 0;">
        <h1 style="font-size:3.5rem;font-weight:900;color:white;margin-bottom:0.5rem;">
            🤖 AutoAgentHire
        </h1>
        <p style="font-size:1.3rem;color:rgba(255,255,255,0.9);margin-bottom:2rem;">
            AI-Powered LinkedIn Job Application Automation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status badges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="text-align:center;"><span class="status-badge status-active">✓ Active Jobs: 0</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align:center;"><span class="status-badge status-pending">📊 Applications: 0</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="text-align:center;"><span class="status-badge status-paused">📈 Success Rate: 0%</span></div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Dashboard", "📋 Applications", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # API Status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
    
    # Main content based on navigation
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📋 Applications":
        show_applications()
    elif page == "⚙️ Settings":
        show_settings()


def show_dashboard():
    """Display the main dashboard."""
    
    # Quick Start Section
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#1f2937;font-weight:700;font-size:2rem;">🚀 Quick Start AutoAgent</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6b7280;margin-bottom:2rem;">Start LinkedIn job automation with default settings or customize your preferences below.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        keywords_quick = st.text_input("Job Title", value="AI Engineer", key="dash_quick_keywords")
    with col2:
        location_quick = st.selectbox("Location", ["Remote", "United States", "India"], key="dash_quick_location")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Start AutoAgent", key="dash_quick_start_btn", use_container_width=True):
            payload = {
                "keywords": keywords_quick,
                "location": location_quick,
                "linkedin_email": st.session_state.get("dash_li_email", ""),
                "linkedin_password": st.session_state.get("dash_li_password", ""),
                "submit": False  # Quick start uses preview mode
            }
            with st.spinner("🤖 Starting AutoAgent..."):
                try:
                    resp = requests.post(f"{API_URL}/api/run-agent", json=payload, timeout=10)
                    if resp.status_code == 200:
                        st.success("Agent started! Check the status below.")
                    else:
                        st.error(f"Failed to start agent: {resp.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Dashboard Content
    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="section-header">🎯 How AutoAgentHire Works</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h4 style="font-size:1.3rem;font-weight:700;color:#1f2937;margin-bottom:1rem;">1. Upload Resume</h4>
            <p style="color:#6b7280;">Upload your PDF resume for AI-powered analysis and skill extraction</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h4 style="font-size:1.3rem;font-weight:700;color:#1f2937;margin-bottom:1rem;">2. AI Analysis</h4>
            <p style="color:#6b7280;">Gemini AI analyzes job compatibility and makes intelligent decisions</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h4 style="font-size:1.3rem;font-weight:700;color:#1f2937;margin-bottom:1rem;">3. Auto Apply</h4>
            <p style="color:#6b7280;">Automated applications to matching positions on LinkedIn</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Advanced Configuration
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#1f2937;font-weight:700;font-size:2rem;">⚙️ Advanced Configuration</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("LinkedIn Email", key="dash_li_email", placeholder="your@email.com")
        adv_keywords = st.text_input("Job Keywords", value="AI Engineer, Machine Learning", key="dash_adv_keywords")
    with col2:
        st.text_input("LinkedIn Password", type="password", key="dash_li_password")
        adv_location = st.text_input("Location", value="Remote", key="dash_adv_location")
    
    preview_mode = st.checkbox("Preview Mode (Don't submit applications)", value=True, key="dash_preview_mode")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Run AutoAgent Automation", key="dash_run_agent_main", use_container_width=True):
        payload = {
            "keywords": adv_keywords,
            "location": adv_location,
            "linkedin_email": st.session_state.get("dash_li_email", ""),
            "linkedin_password": st.session_state.get("dash_li_password", ""),
            "submit": not preview_mode
        }
        
        with st.spinner("🤖 Starting AutoAgent..."):
            try:
                resp = requests.post(f"{API_URL}/api/run-agent", json=payload, timeout=10)
                if resp.status_code == 200:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Poll status
                    for i in range(30):
                        time.sleep(1)
                        try:
                            s = requests.get(f"{API_URL}/api/agent/status", timeout=5).json()
                            status = s.get('status', 'unknown')
                            detail = s.get('detail', {})
                            
                            progress = min((i + 1) * 3, 100)
                            progress_bar.progress(progress)
                            
                            phase = detail.get('phase', '') if isinstance(detail, dict) else ''
                            status_text.markdown(f'''
                            <div style="text-align:center;padding:1rem;background:rgba(255,255,255,0.1);border-radius:12px;margin:1rem 0;">
                                <span style="color:white;font-size:1.2rem;font-weight:600;">
                                    Status: {status.capitalize()} {f"- {phase}" if phase else ""}
                                </span>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                            if status in ('completed', 'failed'):
                                break
                        except:
                            pass
                    
                    final = requests.get(f"{API_URL}/api/agent/status", timeout=5).json()
                    if final.get('status') == 'completed':
                        st.success("✅ Agent run completed successfully!")
                        if preview_mode:
                            st.info("📋 Preview mode: No applications were submitted. Check the results below.")
                        else:
                            st.success("🎉 Applications submitted! Check Applications tab for details.")
                    else:
                        st.error(f"❌ Agent ended with status: {final.get('status')}")
                else:
                    st.error(f"Failed to start agent: {resp.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_applications():
    """Display applications page."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("📋 Applications")
    st.info("Application history will appear here once you run the automation.")
    st.markdown('</div>', unsafe_allow_html=True)


def show_settings():
    """Display settings page."""
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("⚙️ Settings")
    st.write("Configure your preferences here.")
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
