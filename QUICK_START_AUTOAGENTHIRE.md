# 🚀 AutoAgentHire - Quick Start Guide

## Step 1: Check Your Configuration

Your system is already configured with:
- ✅ LinkedIn Email: `sathwikadigoppula888@gmail.com`
- ✅ LinkedIn Password: Configured
- ✅ Gemini API Key: Configured

## Step 2: Start the Backend Server

Open a terminal and run:

```bash
cd /Users/sathwikadigoppula/Documents/GitHub/LinkedIn-Job-Automation-with-AI

# Start the server
./run_autoagenthire.sh
```

This will:
1. ✅ Check Python version
2. ✅ Activate virtual environment
3. ✅ Install dependencies
4. ✅ Install Playwright browsers
5. ✅ Start FastAPI server on port 50501

## Step 3: Open the Frontend UI

**Option 1: Double-click the HTML file**
```
Open: autoagenthire.html
```

**Option 2: Direct link**
```
Open: frontend/autoagenthire/index.html
```

**Option 3: Serve with Python**
```bash
# In a new terminal
cd /Users/sathwikadigoppula/Documents/GitHub/LinkedIn-Job-Automation-with-AI
python3 -m http.server 8080

# Then open: http://localhost:8080/autoagenthire.html
```

## Step 4: Use the Application

### 📄 Upload Your Resume
1. Drag and drop your PDF resume
2. Or click the upload area to browse

### ⚙️ Configure Job Preferences

**🔍 Basic Tab:**
- Job Role: e.g., "AI Engineer", "Data Scientist"
- Location: "Remote", "United States", etc.
- Key Skills: "Python, Machine Learning, AI"

**💼 Details Tab:**
- Experience Level: Entry/Associate/Mid-Senior/Director
- Job Type: Full-time/Part-time/Contract
- Salary Range: $40k - $150k+

**🎯 Advanced Tab:**
- Max Jobs: 1-50 (start with 5-10)
- Similarity Threshold: 0.0-1.0 (recommended: 0.6)
- Auto Apply: ✅ Enabled

### 🚀 Run the Automation

1. Click the big purple button: "🚀 Run AutoAgent - Start Job Hunting"
2. Watch the progress bar and real-time logs
3. Wait for completion (5-15 minutes depending on jobs)
4. Review results with metrics and job cards

## Step 5: Review Results

After completion, you'll see:

📊 **Metrics Dashboard**
- Jobs Found
- Jobs Analyzed
- Applications Sent
- Success Rate

📋 **Job Cards**
- Job title and company
- Location
- Match score (0-100%)
- Application status

💾 **Reports**
- Saved in: `reports/autoagenthire_YYYYMMDD_HHMMSS.json`
- Contains full details of all jobs and applications

---

## 🎯 Example Usage

### Scenario 1: AI Engineer Job Hunt
```
Resume: your_resume.pdf
Keyword: "AI Engineer"
Location: "Remote"
Skills: "Python, Machine Learning, TensorFlow, PyTorch"
Experience: "Mid-Senior level"
Max Jobs: 10
Threshold: 0.7
Auto Apply: ✅

Expected Results:
- Find: 30-50 jobs
- Analyze: 30-50 jobs
- Top Selected: 5-8 jobs
- Apply: 4-6 successful
- Duration: 8-12 minutes
```

### Scenario 2: Entry Level Data Science
```
Resume: your_resume.pdf
Keyword: "Data Scientist"
Location: "United States"
Skills: "Python, R, SQL, Pandas"
Experience: "Entry level"
Job Type: "Full-time"
Max Jobs: 15
Threshold: 0.5
Auto Apply: ✅

Expected Results:
- Find: 40-60 jobs
- Analyze: 40-60 jobs
- Top Selected: 8-12 jobs
- Apply: 6-10 successful
- Duration: 10-15 minutes
```

---

## 🔍 What Happens Behind the Scenes

### Phase 1: Browser Automation (1-2 min)
```
[10:30:00] 🌐 Launching browser...
[10:30:05] ✅ Browser initialized
[10:30:10] 🔐 Logging into LinkedIn...
[10:30:20] ✅ Successfully logged in
```

### Phase 2: Job Search (1-2 min)
```
[10:30:25] 🔍 Searching for "AI Engineer" in "Remote"...
[10:30:30] ✨ Applying Easy Apply filter...
[10:30:35] ✅ Easy Apply filter activated
[10:30:40] 📊 Collecting job listings...
```

### Phase 3: Job Collection (2-3 min)
```
[10:30:50] 🔢 Found 47 job cards
[10:31:00] ✅ Collected: Senior AI Engineer at TechCorp
[10:31:10] ✅ Collected: ML Engineer at DataInc
[10:31:20] ✅ Collected: AI Researcher at AILabs
... (continues for 30 jobs)
```

### Phase 4: AI Analysis (2-4 min)
```
[10:33:00] 🤖 Analyzing: Senior AI Engineer - Score: 87%
[10:33:05] 🤖 Analyzing: ML Engineer - Score: 82%
[10:33:10] 🤖 Analyzing: AI Researcher - Score: 78%
... (continues with AI scoring)
[10:35:00] ✨ Selected 5 jobs for application
```

### Phase 5: Auto-Apply (3-6 min)
```
[10:35:10] 🚀 Applying to: Senior AI Engineer at TechCorp
[10:35:20] 📄 Filling application page 1...
[10:35:30] 📄 Filling application page 2...
[10:35:40] ✅ Submitting application...
[10:35:50] 🎉 Successfully applied!
... (repeats for each job)
```

### Phase 6: Completion
```
[10:42:00] 📊 Automation Complete!
[10:42:00] Jobs Found: 47
[10:42:00] Jobs Analyzed: 47
[10:42:00] Applications Attempted: 5
[10:42:00] Applications Successful: 4
[10:42:00] Success Rate: 80%
[10:42:00] 💾 Report saved: reports/autoagenthire_20241015_104200.json
```

---

## 🛠️ Troubleshooting

### Problem: Server won't start
```bash
# Solution 1: Check if port is in use
lsof -i :50501
kill -9 <PID>  # Kill the process using the port

# Solution 2: Use different port
API_PORT=50502 ./run_autoagenthire.sh
```

### Problem: LinkedIn login fails
```bash
# Solution 1: Check credentials
cat .env | grep LINKEDIN

# Solution 2: Run with visible browser
# Edit .env and set:
HEADLESS_MODE=false

# Solution 3: Handle 2FA manually
# When 2FA appears, complete it manually
# The bot will wait 60 seconds
```

### Problem: No jobs found
```bash
# Solution 1: Try broader search
Keyword: "Engineer" (instead of "Senior AI Engineer")
Location: "United States" (instead of specific city)

# Solution 2: Check filters
- Remove experience level filter
- Remove salary filter
- Ensure Easy Apply is working
```

### Problem: Applications fail
```bash
# Solution 1: Reduce max jobs
Max Jobs: 3 (instead of 15)

# Solution 2: Increase delays
# The bot already has random delays
# But LinkedIn might still detect automation

# Solution 3: Review error logs
cat reports/autoagenthire_*.json | grep "error"

# Solution 4: Manual review
# Some jobs require manual intervention
# This is expected and normal
```

### Problem: AI analysis fails
```bash
# Solution 1: Check Gemini API key
echo $GEMINI_API_KEY

# Solution 2: Test Gemini API
python3 -c "
import google.generativeai as genai
genai.configure(api_key='$GEMINI_API_KEY')
model = genai.GenerativeModel('gemini-2.0-flash-exp')
print(model.generate_content('Hello').text)
"

# Solution 3: Use fallback
# If Gemini fails, bot uses keyword matching
# This is automatic, no action needed
```

---

## 📈 Tips for Best Results

### 🎯 Resume Optimization
1. **Format**: Use PDF format only
2. **Length**: Keep to 1-2 pages
3. **Skills**: Have a dedicated skills section
4. **Keywords**: Match job market keywords
5. **Quantify**: Use numbers (e.g., "Increased performance by 40%")

### 🔍 Search Strategy
1. **Start Small**: Begin with max_jobs=5
2. **Specific Keywords**: Use exact job titles
3. **Realistic Location**: Match your actual location or "Remote"
4. **Threshold**: Start with 0.6, adjust based on results
5. **Review First**: Check applications manually after first run

### ⚙️ Configuration
1. **Personal Info**: Update .env with real information
2. **Phone Number**: Use actual phone for callbacks
3. **LinkedIn URL**: Include your profile link
4. **Portfolio**: Add if you have one

### 🕐 Timing
1. **Best Time**: Weekday mornings (9-11 AM)
2. **Avoid**: Late nights, weekends
3. **Frequency**: Max 2-3 runs per day
4. **Spacing**: Wait 4-6 hours between runs

### 🤖 Automation Ethics
1. **Review Applications**: Always check what was sent
2. **Follow Up**: Respond to any messages
3. **Don't Spam**: Limit applications per company
4. **Be Honest**: Ensure resume accuracy
5. **Manual Touch**: Personalize cover letters

---

## 📊 Expected Performance

| Metric | Typical Range | Your Target |
|--------|---------------|-------------|
| Jobs Found | 30-60 | 40+ |
| Analysis Accuracy | 80-95% | 85%+ |
| Application Success | 70-90% | 75%+ |
| Time per Job | 30-60s | 45s |
| Total Duration | 8-15 min | 10 min |

---

## 🎉 Success Checklist

Before you start:
- [ ] Backend server running on port 50501
- [ ] Frontend UI loaded in browser
- [ ] Resume uploaded (PDF format)
- [ ] Job preferences configured
- [ ] LinkedIn credentials verified
- [ ] Gemini API key tested

During automation:
- [ ] Browser opens successfully
- [ ] LinkedIn login succeeds
- [ ] Jobs appear in search results
- [ ] Easy Apply filter active
- [ ] AI analysis running
- [ ] Applications submitting

After completion:
- [ ] Metrics displayed correctly
- [ ] Job cards showing results
- [ ] Report saved to reports/
- [ ] Success rate > 70%
- [ ] No critical errors

---

## 🚨 Emergency Stop

If something goes wrong:

1. **Stop Backend Server**
   ```bash
   # Press Ctrl+C in terminal
   ```

2. **Close Browser**
   ```bash
   # Close the Chromium window
   # Or kill process:
   pkill -f chromium
   ```

3. **Check Logs**
   ```bash
   # View latest report
   ls -lt reports/ | head -1
   cat reports/autoagenthire_*.json
   ```

4. **Reset and Retry**
   ```bash
   # Start fresh
   ./run_autoagenthire.sh
   ```

---

## 📞 Need Help?

1. Check this guide
2. Review [AUTOAGENTHIRE_README.md](AUTOAGENTHIRE_README.md)
3. Check API docs: http://127.0.0.1:50501/docs
4. Review error logs in `reports/`

---

## 🎯 Next Steps

After successful first run:

1. ✅ Review applications in LinkedIn
2. ✅ Track responses in spreadsheet
3. ✅ Adjust threshold based on results
4. ✅ Refine job keywords
5. ✅ Schedule daily runs
6. ✅ Monitor success rate

---

**You're all set! Ready to automate your job search? 🚀**

```bash
# Let's go!
./run_autoagenthire.sh
```
