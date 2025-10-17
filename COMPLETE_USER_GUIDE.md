# AutoAgentHire - Complete Setup & User Guide

## 🎯 Project Overview

AutoAgentHire is an intelligent, automated job application system that leverages AI (Google Gemini) to streamline your LinkedIn job search and application process. The system features:

- **AI-Powered Job Matching**: Gemini AI evaluates job compatibility with your resume
- **Automated LinkedIn Job Search**: Finds relevant "Easy Apply" positions
- **Smart Cover Letter Generation**: Creates personalized cover letters for each application
- **Intelligent Form Filling**: AI answers application questions contextually
- **Secure Credential Management**: Session-only storage, never persisted
- **Real-time Progress Tracking**: Watch the automation work in real-time
- **Preview Mode**: Test and evaluate before submitting actual applications

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│                                                              │
│  ┌──────────────────┐        ┌───────────────────┐         │
│  │  Streamlit UI    │   OR   │   React (Future)  │         │
│  │  - Forms         │        │   - Dashboard     │         │
│  │  - Progress      │        │   - Analytics     │         │
│  └──────────────────┘        └───────────────────┘         │
└───────────────────────────────────────────────────────────────┘
                            │
                            ▼ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                    Backend Layer (FastAPI)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           API Routes & Controllers                      │ │
│  │  - /api/run-agent     - /api/upload-resume            │ │
│  │  - /api/agent/status  - /api/generate-cover-letter    │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│                            ▼                                 │
│  ┌─────────────────────────────────────────────┐           │
│  │         Agent Orchestrator                   │           │
│  │  - Workflow Coordination                     │           │
│  │  - State Management                          │           │
│  └─────────────────────────────────────────────┘           │
│           │              │               │                   │
│           ▼              ▼               ▼                   │
│  ┌──────────┐   ┌──────────────┐  ┌──────────┐            │
│  │  Search  │   │   Analysis    │  │  Apply   │            │
│  │  Agent   │   │   Agent       │  │  Agent   │            │
│  └──────────┘   └──────────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────────┘
                     │              │
                     ▼              ▼
┌──────────────────────┐  ┌────────────────────────┐
│  Automation Layer    │  │    AI/LLM Layer        │
│                      │  │                        │
│  - Playwright        │  │  - Google Gemini       │
│  - LinkedIn Bot      │  │  - Cover Letter Gen    │
│  - Form Filling      │  │  - Job Matching        │
│  - Navigation        │  │  - Question Answering  │
└──────────────────────┘  └────────────────────────┘
          │
          ▼
┌──────────────────────┐
│   LinkedIn Website   │
│   - Job Search       │
│   - Easy Apply       │
└──────────────────────┘
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for React frontend, optional)
- **Google Gemini API Key** (get from: https://makersuite.google.com/app/apikey)
- **LinkedIn Account**

### Step 1: Clone & Install

```bash
# Clone repository
git clone https://github.com/yourusername/LinkedIn-Job-Automation-with-AI.git
cd LinkedIn-Job-Automation-with-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

**Required configurations in `.env`:**

```env
# Google Gemini API Key (REQUIRED)
GOOGLE_API_KEY="your-gemini-api-key-here"

# OpenAI (Optional, fallback)
OPENAI_API_KEY="your-openai-key-optional"

# Database (SQLite by default, change if needed)
DATABASE_URL="sqlite:///./autoagenthire.db"

# Security
SECRET_KEY="your-super-secret-key-change-this"

# Feature Flags
ENABLE_AUTO_APPLY=false  # Set true to actually submit
ENABLE_EMAIL_NOTIFICATIONS=true
```

### Step 3: Start the Application

**Option A: Full Stack (Recommended)**

```bash
# Terminal 1: Start Backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2: Start Frontend
streamlit run frontend/streamlit/app_enhanced.py --server.port 8501
```

**Option B: Quick Script**

```bash
chmod +x startup.sh
./startup.sh
```

**Option C: Docker (Production)**

```bash
docker-compose up -d
```

### Step 4: Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

---

## 📋 User Guide

### First-Time Setup

1. **Navigate to Home Page**
   - Click "🏠 Home" in the sidebar
   - Read the overview and features

2. **Go to Quick Start**
   - Click "🚀 Quick Start"
   - Follow the 3-step wizard

### Using Quick Start

#### Step 1: Upload Resume
- Click "Browse files" and upload your resume (PDF, DOCX, or TXT)
- Wait for AI analysis
- Review the generated summary

#### Step 2: Job Preferences
- **Job Title/Keywords**: Enter the role you're seeking (e.g., "AI Engineer", "Software Developer")
- **Location**: Select your preferred location or "Remote"

#### Step 3: LinkedIn Credentials
- Enter your LinkedIn email and password
- **Security Note**: Credentials are used only for this session and never stored

#### Step 4: Choose Mode
- **Preview Mode** (Recommended for first run):
  - Searches for jobs
  - Evaluates matches
  - Shows results without applying
  - Great for testing and seeing what the AI finds

- **Full Mode**:
  - Searches and evaluates jobs
  - Generates cover letters
  - Actually submits applications
  - Use only after testing preview mode!

#### Step 5: Start Automation
- Click the start button
- Watch real-time progress
- View detailed logs

### Understanding Results

The system will show you:
- **Jobs Found**: Total number of matching positions
- **Match Scores**: AI evaluation of compatibility (0-1 scale)
- **Applications Submitted**: Count of actual submissions
- **Preview Count**: Jobs evaluated in preview mode

### Advanced Configuration

For power users, access "⚙️ Full Configuration" for:

- **Personal Information**: Full name, email, phone
- **Detailed Job Criteria**:
  - Multiple locations
  - Job type filters
  - Experience level
  - Specific skills
- **AI Settings**:
  - Custom Gemini API key
  - Match score threshold
  - Max applications per run
- **Automation Behavior**:
  - Easy Apply only toggle
  - Cover letter generation
  - Application delays

---

## 🤖 How the AI Works

### 1. Resume Analysis
```
Your Resume → Gemini AI → Extracted Skills & Summary
```
- Parses PDF/DOCX to extract text
- AI identifies key skills, experience, achievements
- Generates professional summary

### 2. Job Matching
```
Job Description + Your Resume → Gemini AI → Match Score (0-1)
```
Gemini evaluates:
- **Skills alignment**: Does your experience match requirements?
- **Experience level**: Junior, mid, senior compatibility
- **Location fit**: Remote vs. on-site preferences
- **Cultural fit**: Values, company mission alignment

Output:
```json
{
  "match_score": 0.85,
  "should_apply": true,
  "reasoning": "Strong match - 90% skill overlap, remote position",
  "strengths": ["Python expertise", "ML experience"],
  "concerns": ["May prefer PhD candidates"]
}
```

### 3. Cover Letter Generation
```
Job + Resume + Company → Gemini AI → Personalized Cover Letter
```
AI creates:
- Custom introduction mentioning the company
- Highlights relevant experience from your resume
- Addresses specific job requirements
- Professional closing with call to action

### 4. Question Answering
```
Application Question + Context → Gemini AI → Intelligent Answer
```
Examples:
- "Why do you want to work here?" → Analyzes company mission, your background
- "Describe your experience with X" → Pulls from resume, elaborates
- "What's your expected salary?" → Uses job level, location context

---

## 🔒 Security & Privacy

### What We Do:
✅ Session-only credential storage (memory only)
✅ No database persistence of passwords
✅ Encrypted environment variables
✅ HTTPS for API calls
✅ Human-like automation patterns to avoid detection

### What We Don't Do:
❌ Store LinkedIn passwords
❌ Share credentials with third parties
❌ Log sensitive information
❌ Track your data

### Best Practices:
1. Use strong, unique LinkedIn password
2. Enable 2FA on LinkedIn (the bot can handle it)
3. Run on secure network (avoid public WiFi)
4. Keep API keys in `.env`, never commit them
5. Use preview mode first to test

---

## 📊 Dashboard & Tracking

### Real-Time Monitoring

The dashboard shows:
- **Current Status**: Idle, Running, Completed, Failed
- **Phase**: Login, Searching, Evaluating, Applying
- **Progress Bar**: Visual indication of workflow
- **Live Logs**: Detailed step-by-step actions

### Application History

View all your applications:
- Job title and company
- Date applied
- Match score
- Status (Applied, Skipped, Failed)
- Generated cover letter (downloadable)

### Analytics (Coming Soon)
- Success rate over time
- Best-performing job keywords
- Average match scores
- Application response rates

---

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Gemini API key | - | Yes |
| `OPENAI_API_KEY` | OpenAI fallback | - | No |
| `DATABASE_URL` | Database connection | SQLite | No |
| `SECRET_KEY` | App encryption key | - | Yes |
| `ENABLE_AUTO_APPLY` | Actually submit apps | false | No |
| `MAX_APPLICATIONS_PER_DAY` | Daily limit | 10 | No |
| `PLAYWRIGHT_HEADLESS` | Run browser hidden | true | No |

### Feature Flags

Control what the system does:

```env
ENABLE_AUTO_APPLY=false          # Safety: preview only
ENABLE_COVER_LETTER_GENERATION=true
ENABLE_SMART_MATCHING=true
ENABLE_EMAIL_NOTIFICATIONS=true
ENABLE_DAILY_REPORTS=true
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`
```bash
# Solution: Use different port
uvicorn backend.main:app --port 8001
```

### Frontend Connection Issues

**Error**: `API Disconnected`
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `API_URL` in frontend matches backend port
3. Check firewall settings

### Automation Fails

**Issue**: Login fails
- Verify credentials are correct
- Check if LinkedIn requires 2FA verification
- Try running non-headless to see what's happening: `PLAYWRIGHT_HEADLESS=false`

**Issue**: Jobs not found
- Make sure keywords match actual job titles
- Try broader search terms
- Check LinkedIn directly to verify jobs exist

**Issue**: Applications skip
- Review match score threshold (lower if too restrictive)
- Check error logs for specific reasons
- Some jobs may not support Easy Apply

### AI Not Working

**Issue**: "Gemini API not available"
1. Verify `GOOGLE_API_KEY` in `.env`
2. Test API key: https://makersuite.google.com/app/apikey
3. Check API quota limits

**Fallback**: System uses default responses if AI fails

---

## 🔧 Advanced Usage

### Running Headless (Production)

```bash
# Backend as service
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Frontend as service  
nohup streamlit run frontend/streamlit/app_enhanced.py --server.port 8501 &
```

### Scheduling Daily Automation

```bash
# Cron job (runs daily at 9 AM)
0 9 * * * cd /path/to/autoagenthire && ./startup.sh
```

### Custom AI Prompts

Edit `backend/llm/gemini_service.py` to customize:
- Cover letter tone and structure
- Job matching criteria
- Question answering style

### Database Integration

For production, use PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/autoagenthire
```

Run migrations:
```bash
alembic upgrade head
```

---

## 📈 Best Practices

### First Run Checklist
- [ ] Use **Preview Mode**
- [ ] Start with broad keywords
- [ ] Set low match threshold (0.5-0.6)
- [ ] Limit to 5-10 jobs
- [ ] Review results carefully

### Optimization Tips
1. **Resume Quality**: Clear, well-formatted resume = better AI analysis
2. **Keyword Strategy**: Use exact job titles from LinkedIn
3. **Location Preferences**: Be specific for better matches
4. **Match Threshold**: 0.7+ for quality, 0.5+ for quantity
5. **Daily Limits**: Don't exceed 10-20 applications per day

### Avoiding LinkedIn Blocks
- Use realistic delays (already built-in)
- Don't run continuously 24/7
- Vary your search patterns
- Pause if you see CAPTCHAs
- Run during business hours

---

## 🆘 Support & Contributing

### Get Help
- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions, share tips
- **Email**: support@autoagenthire.com

### Contributing
We welcome contributions!

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black backend/ frontend/

# Lint
flake8 backend/
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🎉 Success Stories

> "AutoAgentHire helped me apply to 50+ jobs in one afternoon. I got 5 interviews in the first week!" - Sarah K.

> "The AI-generated cover letters are actually good. Better than what I was writing manually!" - Mike T.

> "Preview mode saved me from applying to jobs I wouldn't want. The matching is surprisingly accurate." - Jennifer L.

---

## 🗺️ Roadmap

### Version 2.0 (Coming Soon)
- [ ] Multi-platform support (Indeed, Glassdoor)
- [ ] Email notification system
- [ ] Advanced analytics dashboard
- [ ] Resume builder integration
- [ ] Interview preparation AI
- [ ] Salary negotiation assistant

### Version 3.0 (Future)
- [ ] Mobile app (iOS/Android)
- [ ] Voice-based job search
- [ ] Video interview practice
- [ ] Career path recommendations
- [ ] Networking automation

---

**Last Updated**: October 2025
**Version**: 1.0.0
**Author**: AutoAgentHire Team
