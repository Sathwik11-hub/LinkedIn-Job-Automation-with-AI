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

The project follows a modular, scalable architecture:

```
AutoAgentHire/
├── backend/              # FastAPI backend with AI agents
│   ├── agents/           # AI agent implementations
│   ├── orchestration/    # Multi-agent coordination
│   ├── services/         # Business logic layer
│   ├── models/           # Domain models
│   ├── api/              # API integrations
│   ├── routes/           # FastAPI routes
│   ├── middleware/       # Custom middleware
│   └── database/         # Database models & schemas
├── frontend/             # Streamlit & React UI
├── tests/                # Unit, integration, and e2e tests
├── data/                 # Data storage (logs, uploads, vector DB)
├── deployment/           # Kubernetes & deployment configs
├── alembic/              # Database migrations
├── config/               # Configuration files
└── docs/                 # Documentation
```

For detailed structure, see [Project Structure Documentation](docs/PROJECT_STRUCTURE.md).

### Tech Stack

**Backend:**
- FastAPI (API framework)
- CrewAI/LangGraph (Agent orchestration)
- OpenAI GPT-4, Anthropic Claude, Google Gemini (LLMs)
- ChromaDB/Pinecone (Vector database)
- PostgreSQL (Relational database)
- Neo4j (Graph database - optional)
- Redis (Caching)
- Selenium/Playwright (Web automation)

**Frontend:**
- Streamlit (Quick dashboard)
- React + Vite (Advanced UI)

**AI/ML:**
- LangChain (LLM framework)
- Sentence Transformers (Embeddings)
- spaCy/NLTK (NLP)

**DevOps:**
- Docker & Docker Compose
- Kubernetes
- Alembic (Database migrations)
- GitHub Actions (CI/CD)

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
make db-upgrade
# Or manually: alembic upgrade head
```

6. **Verify setup**
```bash
python scripts/verify_setup.py
```

7. **Run the application**

Backend:
```bash
make run-dev
# Or: uvicorn backend.main:app --reload
```

Streamlit Frontend:
```bash
make streamlit
# Or: streamlit run frontend/streamlit/app.py
```

React Frontend (optional):
```bash
cd frontend/react
npm install
npm run dev
```

## 🛠️ Development Commands

The project includes a comprehensive Makefile for common development tasks:

```bash
# Setup and Installation
make install          # Install production dependencies
make install-dev      # Install development dependencies
make setup           # Initial project setup

# Running the Application
make run             # Run backend in development mode
make run-dev         # Run with auto-reload and debug
make streamlit       # Run Streamlit frontend

# Database Management
make db-migrate      # Create new migration (requires msg="description")
make db-upgrade      # Apply migrations
make db-downgrade    # Rollback migration
make db-current      # Show current revision

# Code Quality
make format          # Format code with black and isort
make lint            # Run flake8 linter
make type-check      # Run mypy type checker
make security-check  # Run bandit security scanner
make quality         # Run all quality checks

# Testing
make test            # Run all tests
make test-unit       # Run unit tests only
make test-integration # Run integration tests
make test-e2e        # Run end-to-end tests
make test-cov        # Run with coverage report

# Docker
make docker-build    # Build Docker images
make docker-up       # Start containers
make docker-down     # Stop containers
make docker-logs     # View logs

# Utilities
make clean           # Clean cache and temp files
make help            # Show all available commands
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
