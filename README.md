# AutoAgentHire 🤖💼

> An autonomous AI agent system that automates job discovery and applications using Agentic AI, LLMs, RAG, and web automation.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

- **🔍 Intelligent Job Discovery**: AI agents automatically search and discover relevant job opportunities
- **🎯 Smart Job Matching**: Advanced matching algorithm using embeddings and semantic similarity
- **📝 Auto-Generated Cover Letters**: Personalized cover letters using RAG and GPT-4
- **🤖 Application Automation**: Automated form filling and application submission
- **📊 Analytics Dashboard**: Track applications, match scores, and success rates
- **🔐 Secure Credential Management**: Encrypted storage of sensitive information
- **📧 Smart Notifications**: Email alerts for new matches and application updates

## 🏗️ Architecture

```
AutoAgentHire/
├── backend/          # FastAPI backend with AI agents
├── frontend/         # Streamlit & React UI
├── database/         # PostgreSQL schemas and migrations
├── vector_db/        # ChromaDB for embeddings
├── tests/           # Unit, integration, and e2e tests
└── docs/            # Documentation
```

### Tech Stack

**Backend:**
- FastAPI (API framework)
- CrewAI/LangGraph (Agent orchestration)
- OpenAI GPT-4 (LLM)
- ChromaDB/Pinecone (Vector database)
- PostgreSQL (Relational database)
- Selenium/Playwright (Web automation)

**Frontend:**
- Streamlit (Quick dashboard)
- React + Vite (Advanced UI)

**AI/ML:**
- LangChain (LLM framework)
- Sentence Transformers (Embeddings)
- spaCy (NLP)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for React frontend)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/autoagenthire.git
cd autoagenthire
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Initialize database**
```bash
python scripts/setup_db.py
alembic upgrade head
```

6. **Run the application**

Backend:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Options:**

Option A - Streamlit (Simple Dashboard):
```bash
streamlit run frontend/streamlit/autoagent_app.py --server.port 8501
```

Option B - React (Modern UI):
```bash
cd frontend/react
npm install
npm run dev
```

Or use the convenience scripts:
```bash
./start_react_frontend.sh
```

React Frontend (optional):
```bash
cd frontend/react
npm install
npm run dev
```

## 📋 Usage

### 1. Upload Your Resume
Upload your resume in PDF, DOCX, or TXT format through the dashboard.

### 2. Configure Job Preferences
Set your preferences:
- Job titles and keywords
- Desired locations
- Experience level
- Salary expectations

### 3. Start Job Search
Trigger the AI agents to:
- Search multiple job boards
- Analyze job descriptions
- Calculate match scores
- Rank opportunities

### 4. Review and Apply
- Review matched jobs with AI-generated insights
- Customize cover letters
- Auto-fill application forms
- Track application status

## 🎨 Frontend Options

AutoAgentHire offers two frontend interfaces to suit different preferences:

### Streamlit Dashboard (Quick & Simple)
- **Port**: http://localhost:8501
- **Features**: Simple dashboard for quick job automation
- **Best for**: Users who want a straightforward interface
- **Startup**: `streamlit run frontend/streamlit/autoagent_app.py`

### React App (Modern & Interactive)
- **Port**: http://localhost:3000
- **Features**: Modern glassmorphism UI with animations
- **Best for**: Users who prefer a polished, interactive experience
- **Technologies**: Next.js, Tailwind CSS, Lucide Icons
- **Startup**: `./start_react_frontend.sh` or `cd frontend/react && npm run dev`

**Key React Features:**
- 🎨 Beautiful glassmorphism design
- 📱 Fully responsive layout
- ⚡ Real-time progress tracking
- 🎯 Interactive job results
- 🚀 Smooth animations and transitions

## 🤖 AI Agents

### Job Search Agent
- **Role**: Job Discovery Specialist
- **Goal**: Find relevant job opportunities
- **Tools**: Web search, database queries

### Analysis Agent
- **Role**: Job Fit Analyzer
- **Goal**: Evaluate job-candidate compatibility
- **Tools**: Vector search, resume analysis, skill matching

### Application Agent
- **Role**: Application Automation Specialist
- **Goal**: Submit high-quality applications
- **Tools**: Cover letter generation, form filling, document upload

## 🔐 Security

- 🔒 Encrypted credential storage using Fernet
- 🔑 JWT-based authentication
- 🛡️ OAuth2 integration (Google, LinkedIn)
- 🚨 Rate limiting and DDoS protection
- 📝 Audit logging for all actions

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Run tests:
```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=backend tests/
```

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

This starts:
- Backend API (port 8000)
- Frontend (port 8501)
- PostgreSQL (port 5432)
- ChromaDB (port 8001)
- Redis (port 6379)

## 📈 Roadmap

- [x] Phase 1: Project Setup
- [x] Phase 2: Database & Models
- [ ] Phase 3: Resume Parser
- [ ] Phase 4: Vector DB & RAG
- [ ] Phase 5: LLM Integration
- [ ] Phase 6: Job Matching Engine
- [ ] Phase 7: Web Automation
- [ ] Phase 8: AI Agents
- [ ] Phase 9: FastAPI Backend
- [ ] Phase 10: Frontend
- [ ] Phase 11: Security
- [ ] Phase 12: Testing
- [ ] Phase 13: Deployment
- [ ] Phase 14: Monitoring
- [ ] Phase 15: Documentation

## ⚠️ Important Notes

- **Terms of Service**: Web scraping and automation may violate job board Terms of Service. Use responsibly.
- **Rate Limiting**: Implement appropriate delays to avoid overwhelming servers.
- **Human Review**: Always review applications before submission.
- **API Costs**: Monitor OpenAI API usage to control costs.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embeddings
- CrewAI for agent framework
- FastAPI community
- All contributors

## 📞 Support

For support, email support@autoagenthire.com or open an issue on GitHub.

---

**Disclaimer**: This tool is for educational purposes. Always comply with job board Terms of Service and use automation ethically and responsibly.
