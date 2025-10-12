# 🤖 AutoAgentHire - Agent Execution Guide

## 📍 **Where to Run the AI Agents**

The AutoAgentHire system provides **4 different ways** to run the AI agents for job automation tasks:

---

## 🎯 **1. Streamlit Web Interface (User-Friendly)**

**🔗 Access**: http://localhost:8504
**👤 Best for**: End users, manual job searches, testing

### How to Use:
1. Open browser to http://localhost:8504
2. Navigate to **"🔍 Job Search"** page
3. Fill out the form:
   - **Keywords**: "Python Developer", "Data Scientist", etc.
   - **Location**: "San Francisco, CA", "Remote", etc.
   - **Experience Level**: Entry/Mid/Senior/Lead
   - **Job Type**: Full-time/Part-time/Contract
4. Click **"🔍 Search Jobs"**
5. View results with match scores and descriptions

### Features:
- ✅ Real-time job search
- ✅ Interactive results display
- ✅ Match scoring
- ✅ Job details and links
- ✅ User-friendly interface

---

## 🚀 **2. FastAPI REST API (Developer-Friendly)**

**🔗 Access**: http://localhost:9000
**👤 Best for**: Developers, integrations, automation

### API Endpoints:

#### **Job Search Agent**
```bash
curl -X POST http://localhost:9000/agents/job-search \
-H "Content-Type: application/json" \
-d '{
  "keywords": "Python Developer",
  "location": "San Francisco, CA", 
  "experience_level": "Senior Level",
  "job_type": "Full-time",
  "max_results": 20
}'
```

#### **API Documentation**
- **Interactive Docs**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc
- **Health Check**: http://localhost:9000/health

### Response Format:
```json
{
  "status": "success",
  "message": "Found 15 job opportunities",
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "TechCorp Inc.",
      "location": "San Francisco, CA",
      "job_type": "Full-time",
      "match_score": 85,
      "url": "https://example.com/job1"
    }
  ],
  "search_criteria": {...}
}
```

---

## 📋 **3. Command Line Interface (Automation-Friendly)**

**📂 Location**: `/run_agents.py`
**👤 Best for**: Scripts, automation, CI/CD, power users

### Usage Examples:

#### **Basic Job Search**
```bash
cd /path/to/LinkedIn-Job-Automation-with-AI
source venv/bin/activate
python run_agents.py search --keywords "Python Developer" --location "San Francisco"
```

#### **Advanced Search with Auto-Apply**
```bash
python run_agents.py search \
  --keywords "ML Engineer" \
  --experience "Senior" \
  --job-type "Full-time" \
  --max-results 50 \
  --auto-apply
```

#### **Remote Jobs Only**
```bash
python run_agents.py search \
  --keywords "DevOps Engineer" \
  --location "Remote" \
  --max-results 30
```

#### **Check System Status**
```bash
python run_agents.py status
```

### Command Options:
- `--keywords, -k`: Job keywords (required)
- `--location, -l`: Job location (default: Remote)
- `--experience, -e`: Experience level (Entry/Mid/Senior/Lead)
- `--job-type, -t`: Job type (Full-time/Part-time/Contract/Internship)
- `--max-results, -m`: Maximum results (default: 50)
- `--auto-apply, -a`: Enable automatic application
- `--user-id, -u`: User identifier (default: cli_user)

---

## 🕒 **4. Scheduled Automation (Background Processing)**

**📂 Location**: `/schedule_agents.py`
**👤 Best for**: Continuous monitoring, background automation

### How to Run:
```bash
cd /path/to/LinkedIn-Job-Automation-with-AI
source venv/bin/activate
python schedule_agents.py
```

### Default Schedule:
- **Daily 9:00 AM**: General Python Developer search
- **Monday 8:00 AM**: Senior Python Developer search (50 results)
- **Friday 5:00 PM**: Machine Learning Engineer search

### Features:
- ✅ Automated daily searches
- ✅ Specialized weekly searches
- ✅ Configurable schedules
- ✅ Background processing
- ✅ Detailed logging

### Customization:
Edit the `default_search_criteria` in `schedule_agents.py`:
```python
self.default_search_criteria = {
    "keywords": "Your Job Title",
    "location": "Your Location",
    "experience_level": "Your Level",
    "job_type": "Full-time",
    "max_results": 20,
    "auto_apply": False  # Set to True for auto-application
}
```

---

## 🔧 **System Status & Monitoring**

### **Check if Services are Running:**
```bash
# Check backend
curl http://localhost:9000/health

# Check frontend
curl http://localhost:8504

# Process status
ps aux | grep -E "(uvicorn|streamlit)"
```

### **Current Running Services:**
- ✅ **Backend API**: http://localhost:9000 (FastAPI)
- ✅ **Frontend UI**: http://localhost:8504 (Streamlit)
- ✅ **API Docs**: http://localhost:9000/docs

---

## 🎯 **Recommended Workflow**

### **For First-Time Users:**
1. Start with **Streamlit Interface** (Method 1)
2. Test job searches manually
3. Review results and tune parameters

### **For Developers:**
1. Use **API endpoints** (Method 2) 
2. Integrate with your applications
3. Automate with scripts

### **For Continuous Automation:**
1. Configure **CLI scripts** (Method 3)
2. Set up **scheduled automation** (Method 4)
3. Monitor results and logs

---

## ⚡ **Quick Start Commands**

```bash
# Start everything
cd LinkedIn-Job-Automation-with-AI
source venv/bin/activate

# Terminal 1: Backend
uvicorn backend.main:app --reload --host 127.0.0.1 --port 9000

# Terminal 2: Frontend  
streamlit run frontend/streamlit/app.py --server.port 8504

# Terminal 3: Run agent
python run_agents.py search --keywords "Python Developer" --location "Remote"

# Terminal 4: Background automation
python schedule_agents.py
```

---

## 🔐 **Configuration Notes**

1. **OpenAI API Key**: Update `.env` file with your actual OpenAI key
2. **LinkedIn Credentials**: Add LinkedIn email/password for automation
3. **Database**: Configure PostgreSQL or use default SQLite
4. **Scheduling**: Customize schedules in `schedule_agents.py`

---

## 🎉 **You're Ready to Go!**

Choose the method that best fits your needs and start automating your job search with AI agents! 🚀