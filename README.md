# AutoAgent Hire — LinkedIn Job Automation with AI

> Autonomous AI agent that discovers, fills, and submits LinkedIn Easy Apply jobs on your behalf.

[![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python%203.11-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%2B%20TypeScript-61dafb?logo=react)](https://vitejs.dev)
[![Automation](https://img.shields.io/badge/Automation-Playwright%20Chromium-45ba4b?logo=playwright)](https://playwright.dev)
[![Deploy](https://img.shields.io/badge/Deploy-Render%20%2B%20Vercel-430098?logo=render)](https://render.com)

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **AI-Powered Form Filling** — Unknown / custom fields answered by AI (GitHub Models ? Groq ? OpenAI fallback with automatic provider detection)
- **Multi-Step Easy Apply** — Handles unlimited form pages with smart Next/Submit detection
- **Field Deduplication** — Each field filled at most once; AI called at most once per label
- **Save-Popup Protection** — Detects and dismisses LinkedIn's "Save this application?" dialog automatically
- **Resume Parsing** — Extracts skills and experience from uploaded PDF/DOCX to prefill forms
- **India-Specific Field Support** — 10th/12th %, College, DOB, Graduation Year, Hometown, CGPA
- **Persistent Browser Profile** — Stays logged in across sessions
- **Dry-Run Mode** — Preview without actually submitting
- **Real-Time Progress** — Frontend polls live status, phase, and per-job results
- **Full Auth System** — JWT-based signup/login, user profiles stored in PostgreSQL

---

## Architecture

```
+---------------------------------------------------------+
¦                    USER BROWSER                         ¦
¦         React + Vite + Tailwind (frontend/lovable)      ¦
¦              Hosted on Vercel (static)                  ¦
+---------------------------------------------------------+
                           ¦ HTTP REST
+--------------------------?------------------------------+
¦                 FastAPI Backend (Python 3.11)            ¦
¦                  Hosted on Render                       ¦
¦                                                         ¦
¦  +--------------+  +--------------+  +--------------+  ¦
¦  ¦  Auth Routes ¦  ¦  V2 Routes   ¦  ¦  Agent API   ¦  ¦
¦  ¦  JWT + bcrypt¦  ¦  Automation  ¦  ¦  LangGraph   ¦  ¦
¦  +--------------+  +--------------+  +--------------+  ¦
¦                           ¦ subprocess (Windows-safe)    ¦
¦  +------------------------?------------------------+    ¦
¦  ¦           playwright_runner.py                   ¦    ¦
¦  ¦  • Field mapping + AI fallback                   ¦    ¦
¦  ¦  • FieldTracker (no re-fills)                    ¦    ¦
¦  ¦  • Multi-step Easy Apply loop                    ¦    ¦
¦  ¦  • Save-popup dismissal                          ¦    ¦
¦  +-------------------------------------------------+    ¦
¦                                                         ¦
¦  PostgreSQL (Supabase)    AI Providers (auto-detected)  ¦
¦  SQLAlchemy models        GitHub Models ? Groq ? OpenAI ¦
+---------------------------------------------------------+
```

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Frontend | React + Vite (TypeScript) | Vercel |
| Backend API | FastAPI + Python 3.11 | Render |
| Database | PostgreSQL | Supabase |
| Browser Automation | Playwright Chromium (subprocess) | Render |
| AI / LLM | GitHub Models / Groq / OpenAI | Cloud APIs |

---

## Project Structure

```
LinkedIn-Job-Automation-with-AI/
¦
+-- backend/                        # All Python backend code
¦   +-- agents/                     # LangGraph automation agents
¦   ¦   +-- playwright_runner.py    ? Core Easy Apply engine (v3)
¦   ¦   +-- autoagenthire_bot.py    ? High-level bot orchestrator
¦   +-- api/                        # Internal API modules
¦   +-- auth/                       # JWT auth (signup/login/middleware)
¦   +-- automation/                 # Form filler & apply handlers
¦   +-- config.py                   # App settings (Pydantic BaseSettings)
¦   +-- database/                   # SQLAlchemy models, CRUD, connections
¦   +-- llm/                        # LLM wrappers
¦   +-- matching/                   # Resume ? job matching
¦   +-- parsers/                    # PDF/DOCX resume parser
¦   +-- playwright_runner.py        ? Easy Apply engine (run as subprocess)
¦   +-- rag/                        # Resume intelligence & vector search
¦   +-- routes/                     # FastAPI route handlers
¦   ¦   +-- v2_routes.py            ? Main automation API (v2)
¦   ¦   +-- auth_routes.py
¦   ¦   +-- ...
¦   +-- utils/                      # Shared utilities
¦   +-- main.py                     # FastAPI app entry point
¦
+-- frontend/
¦   +-- lovable/                    # React + Vite + TypeScript + Tailwind
¦       +-- src/
¦           +-- components/
¦               +-- LinkedInAutomation.tsx  ? Main UI component
¦
+-- scripts/                        # DB init & smoke-test scripts
+-- database/                       # SQL schema (init.sql)
+-- docker/                         # Docker Compose + Dockerfiles
+-- data/                           # Local data (logs, resumes, screenshots)
+-- uploads/                        # Uploaded resumes (gitignored)
¦
+-- build.sh                        # Render build script
+-- Procfile                        # Render web process
+-- render.yaml                     # Render deploy config
+-- requirements.txt                # Python dependencies (single source)
+-- pyrightconfig.json              # Python type-check config
+-- .env.example                    # Environment template
+-- README.md
```

---

## How It Works

### Automation Flow

```
1. User fills form in React UI (profile, resume, keywords, location)
         ¦
2. POST /api/v2/start-automation
   ? Backend spawns playwright_runner.py as a subprocess
         ¦
3. playwright_runner.py:
   +-- Launches Chromium with persistent profile
   +-- Logs into LinkedIn (reuses session if still valid)
   +-- Searches: keywords + location + Easy Apply filter
   +-- Collects up to N job cards
   ¦
   +-- For each job:
       +-- Click Easy Apply button
       +-- LOOP per form step:
       ¦   +-- JS DOM scan ? fill known fields from profile
       ¦   +-- AI fallback ? GitHub Models/Groq for unknown fields
       ¦   +-- Section scan ? radios, textareas, checkboxes
       ¦   +-- Upload resume (once)
       ¦   +-- Validate ? re-fill if validation errors
       ¦   +-- Click Next / Review / Submit
       +-- On completion ? mark job APPLIED / DRY_RUN
         ¦
4. GET /api/v2/automation-status/{id}  ? Frontend polls this
5. GET /api/v2/automation-results/{id} ? Frontend fetches final results
```

### AI Field Handler

When a form field label is not recognized by the built-in mapping:

1. The field label + job title + user profile + resume excerpt are sent to the AI
2. Provider is auto-detected: **GitHub Models** (preferred) ? **Groq** ? **OpenAI**
3. Answer is cached — the AI is called **at most once per unique field label**
4. If the AI returns nothing, the field is skipped gracefully

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (local or Supabase)

### 1. Clone & Install

```bash
git clone https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI.git
cd LinkedIn-Job-Automation-with-AI

# Python virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
playwright install chromium

# Frontend
cd frontend/lovable
npm install
cd ../..
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your values:

```dotenv
# -- LinkedIn ------------------------------------------
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password

# -- AI Keys (at least one required for unknown fields) -
GITHUB_API_KEY=ghp_xxxxxxxxxxxx        # GitHub Personal Access Token
groq_api_key=gsk_xxxxxxxxxxxxxxxxxxxx  # https://console.groq.com
OPENAI_API_KEY=sk-xxxxxxxxxxxx         # Optional fallback

# -- Database ------------------------------------------
DATABASE_URL=postgresql://user:pass@localhost:5432/auto-agent-hire

# -- Auth ----------------------------------------------
SECRET_KEY=your-32-char-random-secret

# -- Job Search Defaults -------------------------------
JOB_KEYWORDS=Software Engineer
JOB_LOCATION=India
MAX_APPLICATIONS=5
TEST_MODE=true          # true = dry run (no submissions)
```

Create `frontend/lovable/.env.local`:

```dotenv
VITE_API_URL=http://localhost:8000
```

### 3. Initialize Database

```bash
python scripts/setup_db.py
```

### 4. Start Servers

```bash
# Terminal 1 — Backend API (http://localhost:8000)
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

# Windows PowerShell
$env:PYTHONPATH="."; .venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend (http://localhost:8080)
cd frontend/lovable && npm run dev
```

Open [http://localhost:8080](http://localhost:8080)

Swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Deployment

### Backend ? Render

1. Push repo to GitHub
2. Go to [render.com](https://render.com) ? **New Web Service** ? connect your repo
3. Render auto-reads `render.yaml` — click **Deploy**
4. Set these **Secret** environment variables in the Render dashboard:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Random 32-char string for JWT |
| `LINKEDIN_EMAIL` | LinkedIn account email |
| `LINKEDIN_PASSWORD` | LinkedIn account password |
| `GITHUB_API_KEY` | GitHub PAT (for AI field filling) |
| `groq_api_key` | Groq API key |
| `OPENAI_API_KEY` | OpenAI key (optional fallback) |
| `CORS_ORIGINS` | Your Vercel URL e.g. `https://yourapp.vercel.app` |

Your backend URL will be: `https://linkedin-automation-backend.onrender.com`

> `render.yaml` runs `build.sh` which installs `requirements.txt` and `playwright install chromium` automatically.

---

### Frontend ? Vercel

1. Go to [vercel.com](https://vercel.com) ? **New Project** ? import your GitHub repo
2. Set **Root Directory** to `frontend/lovable`
3. Add environment variable in Vercel dashboard:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | Your Render backend URL |

4. Click **Deploy**

> Vercel hosts the static React build only. The Python backend runs entirely on Render.

---

### Docker (Self-Hosted)

```bash
# Build and run everything with Docker Compose
cd docker
docker-compose up --build
```

Services start on:
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/auth/signup` | Register new user |
| `POST` | `/auth/login` | Login ? JWT token |
| `POST` | `/api/v2/start-automation` | Start LinkedIn automation |
| `GET` | `/api/v2/automation-status/{id}` | Poll live progress |
| `GET` | `/api/v2/automation-results/{id}` | Fetch final results |
| `POST` | `/api/v1/resume/upload` | Upload resume (PDF/DOCX) |
| `POST` | `/api/run-agent` | Run AI agent pipeline |
| `GET` | `/docs` | Interactive Swagger UI |

---

## Troubleshooting

| Symptom | Solution |
|---------|----------|
| `playwright install` fails on Render | `build.sh` handles this automatically via `render.yaml` |
| CORS error in browser | Set `CORS_ORIGINS=https://yourapp.vercel.app` in Render env vars |
| Database connection refused | Verify `DATABASE_URL` in Render/local `.env` |
| "Save this application?" popup appears | Fixed in v3 — bot auto-dismisses it without using Escape key |
| Unknown form fields left empty | AI fallback active — set `GITHUB_API_KEY` or `groq_api_key` in `.env` |
| Bot keeps re-filling same field | Fixed in v3 — `FieldTracker` prevents any field being processed twice |
| LinkedIn security checkpoint | Run once manually with `headless=false` to complete the challenge |
| `psycopg2` not found | `psycopg2-binary` is in `requirements.txt`; Render installs it automatically |

---

## License

MIT — see [LICENSE](LICENSE).


