# 🏗️ AutoAgentHire System Architecture

## Overview

AutoAgentHire is a production-ready autonomous job application system that uses AI agents to search LinkedIn jobs, analyze job descriptions, match them with resume data, and automatically apply to positions.

This document describes the complete system architecture, components, and implementation.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Agent System](#agent-system)
4. [Security](#security)
5. [Performance](#performance)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Configuration](#configuration)

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  React/Streamlit UI for job preferences, status, reports    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  Authentication │ Job Search │ Applications │ Reports        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                     Agent Orchestrator                       │
│  Coordinates workflow: Parse → Search → Match → Apply       │
└────┬───────────┬──────────┬──────────┬──────────────────────┘
     │           │          │          │
     ↓           ↓          ↓          ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐
│ Resume  │ │   Job   │ │ Matching│ │ Application │
│ Parser  │ │  Search │ │  Agent  │ │    Agent    │
│  Agent  │ │  Agent  │ │         │ │             │
└─────────┘ └─────────┘ └─────────┘ └─────────────┘
     │           │          │          │
     ↓           ↓          ↓          ↓
┌─────────────────────────────────────────────────────────────┐
│              LLM Services (Gemini/OpenAI/GitHub)            │
│  Resume Analysis │ Job Analysis │ Form Filling │ CoverLetter│
└─────────────────────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   Browser Automation                         │
│     Playwright/Selenium for LinkedIn interaction            │
└─────────────────────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│               Data Layer (PostgreSQL/SQLite)                 │
│  Users │ Jobs │ Applications │ Logs │ Credentials           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 Core Components

### 1. Authentication Service

**Location:** `backend/auth/`

**Purpose:** Secure user authentication and credential management

**Features:**
- JWT token-based authentication
- Password hashing with bcrypt
- Credential encryption using Fernet
- Session management
- Multi-user support

**Key Classes:**
- `AuthService` - Authentication and token management
- `CredentialVault` - Secure credential storage
- `middleware.py` - FastAPI authentication dependencies

**Usage:**
```python
from backend.auth import get_auth_service

auth = get_auth_service()
hashed = auth.hash_password("password123")
token = auth.create_session_token(user_id=1, email="user@example.com")
user = auth.verify_session_token(token)
```

---

### 2. Resume Parser Agent

**Location:** `backend/parsers/resume_parser.py`, `backend/agents/nodes/resume_parser.py`

**Purpose:** Extract skills, experience, and education from resumes

**Features:**
- Supports PDF, DOCX, TXT formats
- AI-powered extraction using LLMs
- Caching for performance
- Structured output (skills, experience, education)

**Flow:**
```
Resume File → Parse Text → Extract with LLM → Structure Data → Cache
```

---

### 3. Job Search Agent

**Location:** `backend/agents/job_search_agent.py`, `backend/agents/autoagenthire_bot.py`

**Purpose:** Search LinkedIn for relevant jobs

**Features:**
- LinkedIn Easy Apply filter
- Location and keyword-based search
- Anti-detection browser automation
- Persistent browser profiles
- Job detail extraction

**Search Flow:**
```
Login → Navigate to Jobs → Apply Filters → Scroll & Collect → Extract Details
```

---

### 4. Job Analysis Agent

**Location:** `backend/matching/job_filter_production.py`

**Purpose:** Analyze job descriptions and requirements

**Features:**
- Role taxonomy classification
- Required skills extraction
- Experience level detection
- Company information parsing
- Freshness scoring

---

### 5. Matching Agent

**Location:** `backend/agents/nodes/job_matching.py`, `backend/matching/`

**Purpose:** Score job-resume compatibility

**Algorithm:**
```
Score = (Skill Match × 0.4) +
        (Experience Match × 0.3) +
        (Role Relevance × 0.2) +
        (Location Match × 0.1)
```

**Features:**
- Skill-based matching
- Experience level comparison
- Location preferences
- Minimum threshold filtering

---

### 6. Application Agent

**Location:** `backend/agents/application_agent.py`, `backend/automation/linkedin_auto_apply.py`

**Purpose:** Automate LinkedIn Easy Apply process

**Features:**
- Multi-step form handling
- Dynamic field detection (text, dropdown, file upload)
- AI-powered question answering
- Resume upload
- Cover letter generation
- Submission verification

**Application Flow:**
```
Open Job → Click Easy Apply → Fill Fields → Upload Resume → 
Generate Cover Letter → Review → Submit → Verify
```

---

### 7. Cover Letter Agent

**Location:** `backend/llm/cover_letter_generator.py`

**Purpose:** Generate personalized cover letters

**Features:**
- Job-specific customization
- Resume context integration
- Professional tone
- 150-200 word target
- Multiple LLM support (GPT-4, Gemini)

**Generation Flow:**
```
Job Description + Resume + Skills → LLM Prompt → Generate → Format → Cache
```

---

### 8. Orchestrator Agent

**Location:** `backend/agents/orchestrator.py`, `backend/agents/langgraph_orchestrator.py`

**Purpose:** Coordinate all agents in the workflow

**Workflow:**
```
1. Receive user preferences
2. Trigger Resume Parser Agent
3. Call Job Search Agent
4. Send results to Analysis Agent
5. Call Matching Agent
6. If score > threshold → Application Agent
7. Generate Cover Letter
8. Log results
9. Generate report
```

**Features:**
- LangGraph-based state management
- Error recovery
- Progress tracking
- Performance monitoring
- Parallel execution support

---

## 🔐 Security

### Authentication

**JWT Tokens:**
- 30-day expiration by default
- Includes user_id, email, timestamp
- HMAC-SHA256 signing
- Token verification on protected routes

**Password Security:**
- Bcrypt hashing with automatic salt
- Configurable cost factor
- No plain text storage
- Secure comparison

**Credential Encryption:**
```python
# LinkedIn passwords and API keys encrypted with Fernet
encrypted = vault.store_linkedin_credentials(user_id, email, password)
# Stored as base64-encoded ciphertext
# Decrypted only when needed
decrypted = vault.retrieve_linkedin_credentials(encrypted)
```

### Protected Endpoints

```python
from backend.auth.middleware import require_auth

@router.get("/protected")
async def protected_route(current_user: dict = Depends(require_auth)):
    # Only accessible with valid JWT token
    return {"user_id": current_user["user_id"]}
```

### Environment Variables

**Never committed:**
- `.env` file in `.gitignore`
- Encryption keys in `data/.encryption_key` (600 permissions)
- JWT secret auto-generated if not provided

---

## ⚡ Performance

### Optimizations Implemented

1. **Parallel Job Processing** - 4x speedup
2. **Resume Caching** - No redundant parsing
3. **Job Listing Cache** - Faster re-runs
4. **Optimized Browser Operations** - 50% faster
5. **Performance Monitoring** - Real-time metrics

**See:** [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md)

### Configuration

```bash
# Performance tuning
PARALLEL_APPLICATIONS=true
MAX_PARALLEL_APPLICATIONS=3
HEADLESS_BROWSER=false
BROWSER_SLOW_MO=50
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### Credentials Table
```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service VARCHAR(100) NOT NULL,  -- 'linkedin', 'gemini', 'github'
    username VARCHAR(255),          -- Email or username
    encrypted_value TEXT NOT NULL,  -- Encrypted password/API key
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Job Listings Table
```sql
CREATE TABLE job_listings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    url VARCHAR(500) UNIQUE,
    easy_apply BOOLEAN DEFAULT FALSE,
    scraped_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### Applications Table
```sql
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    job_id INTEGER REFERENCES job_listings(id),
    status VARCHAR(50) DEFAULT 'draft',  -- draft, applied, rejected, etc.
    cover_letter TEXT,
    custom_responses JSON,
    applied_at TIMESTAMP,
    tracking_info JSON
);
```

**See:** `backend/database/models.py` for complete schema

---

## 🌐 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get token | No |
| GET | `/auth/me` | Get current user | Yes |
| POST | `/auth/credentials/linkedin` | Store LinkedIn creds | Yes |
| GET | `/auth/credentials/linkedin` | Get LinkedIn creds | Yes |

### Automation

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v2/start-automation` | Start job automation | Optional |
| GET | `/api/v2/automation-status/{id}` | Check progress | Optional |
| GET | `/api/v2/automation-results/{id}` | Get results | Optional |

### Job Search

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/jobs/search` | Search jobs | Optional |
| GET | `/jobs/{id}` | Get job details | No |
| POST | `/jobs/match` | Match job with resume | Yes |

**See:** FastAPI `/docs` for interactive documentation

---

## ⚙️ Configuration

### Environment Variables

```bash
# Application
APP_NAME=AutoAgentHire
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///./data/autoagenthire.db
# or PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Authentication
JWT_SECRET_KEY=auto-generated-if-not-set
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days

# LinkedIn
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password

# AI Services
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
GITHUB_API_KEY=your_github_token

# Job Search
JOB_KEYWORDS=Software Engineer
JOB_LOCATION=United States
MAX_APPLICATIONS=5
TEST_MODE=false

# Performance
PARALLEL_APPLICATIONS=true
MAX_PARALLEL_APPLICATIONS=3
HEADLESS_BROWSER=false
BROWSER_SLOW_MO=50
```

### .env File

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
nano .env
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment

```bash
# Edit .env with your credentials
nano .env
```

### 3. Initialize Database

```bash
PYTHONPATH=$PWD python3 -m backend.database.init_db
```

### 4. Start Backend

```bash
PYTHONPATH=$PWD python3 -m uvicorn backend.main:app --port 8000 --reload
```

### 5. Access API

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 📚 Related Documentation

- [README.md](README.md) - Project overview
- [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md) - Performance guide
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization
- [SYSTEM_READY.md](SYSTEM_READY.md) - Quick start

---

## 🔄 Workflow Example

### Complete Automation Flow

```python
# 1. User registers and logs in
POST /auth/register
{
  "email": "user@example.com",
  "password": "secure123",
  "full_name": "John Doe"
}
→ Returns JWT token

# 2. Store LinkedIn credentials
POST /auth/credentials/linkedin
Authorization: Bearer <token>
{
  "email": "linkedin@example.com",
  "password": "linkedin_pass"
}

# 3. Start automation
POST /api/v2/start-automation
Authorization: Bearer <token>
{
  "keywords": "Python Developer",
  "location": "Remote",
  "max_applications": 5,
  "auto_apply": true
}
→ Returns automation_id

# 4. Check status
GET /api/v2/automation-status/{automation_id}
→ Returns progress (20%, 40%, 60%, etc.)

# 5. Get results
GET /api/v2/automation-results/{automation_id}
→ Returns full report with applications
```

---

## 🎯 Best Practices

1. **Always use TEST_MODE=true** for initial testing
2. **Monitor performance metrics** in reports
3. **Keep encryption keys backed up** (`data/.encryption_key`)
4. **Use environment-specific configs** (dev/staging/prod)
5. **Enable parallel processing** for production
6. **Review AI-generated cover letters** before going live
7. **Set appropriate MAX_APPLICATIONS** limits
8. **Check logs regularly** for errors

---

## 🐛 Troubleshooting

### Common Issues

**Authentication errors:**
```bash
# Check JWT secret is set
echo $JWT_SECRET_KEY

# Verify encryption key exists
ls -la data/.encryption_key
```

**Browser automation fails:**
```bash
# Reinstall browser
playwright install chromium

# Clear browser profile
rm -rf browser_profile/*
```

**Performance issues:**
```bash
# Enable parallel processing
export PARALLEL_APPLICATIONS=true

# Check cache statistics in reports
```

---

**Last Updated:** February 1, 2026
**Version:** 1.0.0
**Status:** Production Ready ✅
