# 🤖 AutoAgentHire - Quick Start Guide

## 🚀 Installation & Setup (5 Minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
python3 setup_complete.py
```

This script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup Playwright browsers
- ✅ Create necessary directories
- ✅ Configure environment file

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium

# 4. Create directories
mkdir -p uploads/resumes uploads/cover_letters logs vector_store

# 5. Setup environment
cp .env.example .env
nano .env  # Edit and add your API keys
```

---

## 🔑 Required API Keys

### Google Gemini API Key (REQUIRED)

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to `.env`:
   ```env
   GOOGLE_API_KEY="your-key-here"
   ```

### OpenAI API Key (Optional)

Only needed if you want to use GPT models as fallback:
1. Visit: https://platform.openai.com/api-keys
2. Create new key
3. Add to `.env`:
   ```env
   OPENAI_API_KEY="sk-your-key-here"
   ```

---

## ▶️ Running the Application

### Quick Start (All-in-One)

**macOS/Linux:**
```bash
chmod +x startup.sh
./startup.sh
```

**Windows:**
```cmd
startup.bat
```

### Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
source venv/bin/activate  # Windows: venv\Scripts\activate
streamlit run frontend/streamlit/app_enhanced.py --server.port 8501
```

---

## 🌐 Accessing the Application

Once started:

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📝 First Run Workflow

### Step 1: Upload Resume (30 seconds)
1. Navigate to "🚀 Quick Start"
2. Upload your resume (PDF/DOCX/TXT)
3. Wait for AI analysis
4. Review the generated summary

### Step 2: Set Job Preferences (1 minute)
- **Job Title**: "Software Engineer" or "Data Scientist"
- **Location**: "Remote" or specific city
- Keep it simple for first run!

### Step 3: LinkedIn Credentials (30 seconds)
- Enter your LinkedIn email
- Enter your LinkedIn password
- **Note**: Credentials are session-only, never stored!

### Step 4: Preview Mode (RECOMMENDED)
- ✅ Check "Preview Mode"
- This will find and evaluate jobs WITHOUT applying
- Perfect for testing!

### Step 5: Start Automation (2-5 minutes)
- Click "🔍 Preview Jobs"
- Watch real-time progress
- Review matched jobs and scores

---

## 🎯 Understanding the Results

### Match Scores
- **0.8-1.0**: Excellent match - highly recommended
- **0.6-0.8**: Good match - worth considering
- **0.4-0.6**: Moderate match - review carefully
- **Below 0.4**: Weak match - probably skip

### Status Meanings
- **🔵 Running**: Automation is active
- **🟢 Completed**: Successfully finished
- **🟡 Paused**: Temporarily stopped
- **🔴 Failed**: Error occurred (check logs)

---

## ⚙️ Configuration Tips

### For Your First Run

```env
# .env settings for safe testing
ENABLE_AUTO_APPLY=false          # KEEP FALSE FOR TESTING!
MAX_APPLICATIONS_PER_DAY=5       # Start small
PLAYWRIGHT_HEADLESS=true         # Hide browser window
```

### After You're Comfortable

```env
# When ready to auto-apply
ENABLE_AUTO_APPLY=true           # Enable actual submissions
MAX_APPLICATIONS_PER_DAY=10      # Increase limit
ENABLE_COVER_LETTER_GENERATION=true
```

---

## 🐛 Common Issues & Solutions

### "API Disconnected" Error

**Problem**: Frontend can't reach backend

**Solution**:
```bash
# Check backend is running
curl http://localhost:8000/health

# If not, start it:
uvicorn backend.main:app --reload --port 8000
```

### "Gemini API not available"

**Problem**: API key not configured or invalid

**Solution**:
1. Check `.env` has `GOOGLE_API_KEY=your-actual-key`
2. Verify key at: https://makersuite.google.com/app/apikey
3. Restart the application

### "Login Failed" Error

**Problem**: LinkedIn credentials issue

**Solution**:
1. Verify email/password are correct
2. Check if LinkedIn requires 2FA (manually log in first)
3. Try running non-headless to see what happens:
   ```env
   PLAYWRIGHT_HEADLESS=false
   ```

### "Module not found" Errors

**Problem**: Dependencies not installed

**Solution**:
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## 💡 Pro Tips

### Tip 1: Start with Preview Mode
**Always** use preview mode for your first 2-3 runs to:
- Understand what jobs the AI finds
- See match scores in action
- Verify cover letters are good quality
- Avoid wasting applications

### Tip 2: Optimize Your Resume
The AI works best with:
- Clear section headers (Experience, Education, Skills)
- Bullet points for achievements
- Specific technologies and tools mentioned
- Quantified results (numbers, percentages)

### Tip 3: Use Specific Keywords
Instead of: "Developer"
Use: "React Developer", "Senior Python Engineer", "ML Engineer"

### Tip 4: Set Realistic Limits
- **First Week**: 5-10 applications/day
- **Once comfortable**: 10-20 applications/day
- **Never**: 50+ applications/day (risk of LinkedIn throttling)

### Tip 5: Review Generated Content
Before enabling auto-apply:
1. Run preview mode
2. Check a few cover letters
3. Review AI-generated answers
4. Tweak your resume if needed
5. Then enable auto-apply

---

## 📊 Dashboard Metrics Explained

### Jobs Found
Total number of jobs matching your criteria

### Applications Submitted
Actual applications sent (only in full mode)

### Applications Previewed
Jobs evaluated in preview mode

### Average Match Score
Mean compatibility score across all jobs

### Success Rate
(Will be populated as you get responses)

---

## 🔒 Security Best Practices

### ✅ DO:
- Use strong LinkedIn password
- Keep `.env` file secure
- Run on trusted networks
- Enable LinkedIn 2FA
- Use preview mode first
- Review logs regularly

### ❌ DON'T:
- Share your `.env` file
- Commit `.env` to git
- Use on public WiFi
- Run 24/7 continuously
- Exceed 20 apps/day
- Ignore error messages

---

## 📚 Next Steps

### After Your First Successful Run:

1. **Review Results**
   - Check Dashboard for metrics
   - Review matched jobs
   - Read generated cover letters

2. **Adjust Settings**
   - Tweak match score threshold
   - Modify job keywords
   - Update experience level

3. **Enable Auto-Apply** (when ready)
   - Set `ENABLE_AUTO_APPLY=true` in `.env`
   - Start with low daily limits
   - Monitor results closely

4. **Read Full Documentation**
   - `COMPLETE_USER_GUIDE.md` - Comprehensive guide
   - `README.md` - Project overview
   - `/docs` folder - Technical details

---

## 🆘 Get Help

### Documentation
- **Quick Start**: This file
- **Full Guide**: `COMPLETE_USER_GUIDE.md`
- **API Docs**: http://localhost:8000/docs (when running)

### Support Channels
- **GitHub Issues**: Report bugs, request features
- **Discussions**: Ask questions, share tips
- **Email**: support@autoagenthire.com

### Troubleshooting
- Check `logs/backend.log` for backend errors
- Check `logs/frontend.log` for UI issues
- Check `linkedin_automation.log` for LinkedIn bot logs

---

## ✅ Quick Checklist

Before starting your first run:

- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install chromium`)
- [ ] `.env` file configured with GOOGLE_API_KEY
- [ ] Resume prepared (PDF/DOCX)
- [ ] LinkedIn credentials ready
- [ ] Backend running (port 8000)
- [ ] Frontend running (port 8501)
- [ ] Preview mode enabled (for safety)

---

## 🎉 Ready to Go!

You're all set! Here's what to do now:

1. **Start the application**: `./startup.sh` (or `startup.bat`)
2. **Open browser**: http://localhost:8501
3. **Upload resume**: Click "🚀 Quick Start"
4. **Set preferences**: Job title and location
5. **Enter LinkedIn**: Email and password
6. **Start preview**: Click "🔍 Preview Jobs"
7. **Watch the magic**: Real-time automation!

**First run should take 2-5 minutes and find 5-20 jobs.**

---

**Questions? Issues? Feedback?**

Open an issue on GitHub or check the full documentation!

**Happy job hunting! 🚀**
