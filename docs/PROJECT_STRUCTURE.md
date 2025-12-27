# Project Structure Documentation

This document provides an overview of the AutoAgentHire project structure and organization.

## Directory Layout

```
AutoAgentHire/
│
├── backend/                    # Backend application code
│   ├── agents/                 # AI agent implementations
│   │   ├── orchestrator.py     # Agent coordination
│   │   ├── job_search_agent.py
│   │   ├── analysis_agent.py
│   │   └── application_agent.py
│   │
│   ├── api/                    # API endpoints
│   │   └── linkedin_integration.py
│   │
│   ├── automation/             # Web automation scripts
│   │   └── linkedin_auto_apply.py
│   │
│   ├── database/               # Database models and schemas
│   │   ├── models.py           # SQLAlchemy models
│   │   └── schemas.py          # Pydantic schemas
│   │
│   ├── llm/                    # LLM service integrations
│   │   ├── openai_client.py
│   │   └── gemini_service.py
│   │
│   ├── middleware/             # Custom FastAPI middleware
│   │   └── custom.py           # Logging, error handling, rate limiting
│   │
│   ├── models/                 # Domain models (business logic)
│   │   └── domain.py           # Pydantic domain models
│   │
│   ├── orchestration/          # Agent orchestration logic
│   │   └── orchestrator.py     # Multi-agent coordination
│   │
│   ├── parsers/                # Document parsers
│   │   └── resume_parser.py
│   │
│   ├── rag/                    # Retrieval-Augmented Generation
│   │   └── vector_store.py
│   │
│   ├── routes/                 # API route handlers
│   │   └── api_routes.py
│   │
│   ├── scheduler/              # Task scheduling
│   │
│   ├── security/               # Authentication and security
│   │
│   ├── services/               # Business logic services
│   │   └── job_service.py      # Job, application, resume services
│   │
│   ├── utils/                  # Utility functions
│   │   └── logger.py
│   │
│   ├── config.py               # Application configuration
│   └── main.py                 # FastAPI application entry point
│
├── frontend/                   # Frontend applications
│   ├── streamlit/              # Streamlit dashboard
│   │   └── app.py
│   └── autoagenthire/          # React/Next.js frontend (optional)
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
│
├── data/                       # Data storage
│   ├── logs/                   # Application logs
│   ├── uploads/                # Uploaded files
│   ├── resumes/                # Resume storage
│   ├── job_listings/           # Cached job data
│   ├── templates/              # Document templates
│   └── vector_db/              # Vector embeddings
│
├── database/                   # Database scripts
│   └── init.sql                # Database initialization
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Alembic environment
│   └── script.py.mako          # Migration template
│
├── config/                     # Configuration files
│   └── settings.py             # Additional config settings
│
├── deployment/                 # Deployment configurations
│   ├── kubernetes/             # Kubernetes manifests
│   │   ├── backend-deployment.yaml
│   │   └── config-and-services.yaml
│   └── terraform/              # Terraform IaC (if needed)
│
├── docker/                     # Docker configurations
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── docs/                       # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── USER_GUIDE.md
│
├── scripts/                    # Utility scripts
│   ├── setup_db.py
│   └── setup_complete.py
│
├── .env.example                # Environment variables template
├── .dockerignore               # Docker ignore patterns
├── .gitignore                  # Git ignore patterns
├── alembic.ini                 # Alembic configuration
├── pyproject.toml              # Project metadata and tool configs
├── requirements.txt            # Python dependencies
├── Makefile                    # Common development commands
├── CONTRIBUTING.md             # Contribution guidelines
├── README.md                   # Project overview
└── LICENSE                     # MIT License

```

## Key Components

### 1. Backend (`backend/`)

The backend is organized into modular components:

- **agents/**: AI agent implementations using CrewAI/LangChain
- **orchestration/**: Coordinates multiple agents to accomplish complex tasks
- **services/**: Business logic layer (job search, applications, notifications)
- **models/**: Domain models representing business entities
- **database/**: Database models and schemas (SQLAlchemy + Pydantic)
- **api/**: API integration with external services (LinkedIn, Indeed)
- **routes/**: FastAPI route handlers
- **middleware/**: Custom middleware (logging, auth, rate limiting)
- **automation/**: Web automation with Selenium/Playwright

### 2. Frontend (`frontend/`)

- **streamlit/**: Quick dashboard UI for monitoring and control
- **autoagenthire/**: Advanced React/Next.js UI (optional)

### 3. Tests (`tests/`)

Comprehensive test suite:
- **unit/**: Fast, isolated unit tests
- **integration/**: Component integration tests
- **e2e/**: Full application workflow tests

### 4. Data (`data/`)

Data storage organized by type:
- Logs, uploads, resumes, job listings, templates, vector embeddings

### 5. Deployment (`deployment/`)

Production deployment configurations:
- Kubernetes manifests for container orchestration
- Terraform for infrastructure as code

### 6. Configuration

- **pyproject.toml**: Modern Python project configuration
- **alembic.ini**: Database migration configuration
- **.env.example**: Environment variables template
- **config/settings.py**: Additional application settings

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Agent Orchestration**: CrewAI, LangChain, LangGraph
- **LLM**: OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Vector DB**: ChromaDB, Pinecone
- **Database**: PostgreSQL, Redis
- **Graph DB**: Neo4j (optional)
- **Web Automation**: Selenium, Playwright

### Frontend
- **Dashboard**: Streamlit
- **Advanced UI**: React + Vite (optional)

### AI/ML
- **LangChain**: LLM framework
- **Sentence Transformers**: Embeddings
- **spaCy/NLTK**: NLP processing

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, Prometheus

## Development Workflow

### Setup
```bash
# Install dependencies
make install-dev

# Setup environment
make setup

# Initialize database
make db-upgrade
```

### Development
```bash
# Run backend
make run-dev

# Run frontend
make streamlit

# Run tests
make test

# Code quality
make quality
```

### Deployment
```bash
# Build Docker images
make docker-build

# Deploy to Kubernetes
kubectl apply -f deployment/kubernetes/
```

## Module Descriptions

### Agent System

The agent system is the core of AutoAgentHire:

1. **Job Search Agent**: Discovers job opportunities across platforms
2. **Analysis Agent**: Evaluates job-candidate compatibility using embeddings
3. **Application Agent**: Automates application submission
4. **Orchestrator**: Coordinates agents to execute complex workflows

### Services Layer

Business logic is encapsulated in services:

- **JobService**: Job search, matching, recommendation
- **ApplicationService**: Application creation, tracking, status management
- **ResumeService**: Resume parsing, skill extraction, summarization
- **NotificationService**: Email and in-app notifications

### Data Models

Separation of concerns:
- **Database Models** (`backend/database/models.py`): SQLAlchemy ORM models
- **Domain Models** (`backend/models/domain.py`): Business logic models
- **Schemas** (`backend/database/schemas.py`): Pydantic validation models

## Best Practices

1. **Separation of Concerns**: Clear separation between API, business logic, and data layers
2. **Type Safety**: Use Pydantic for validation and type hints throughout
3. **Async/Await**: Leverage async programming for I/O-bound operations
4. **Testing**: Comprehensive test coverage with unit, integration, and E2E tests
5. **Documentation**: Document all public APIs and complex logic
6. **Security**: Encrypted credentials, JWT auth, rate limiting
7. **Monitoring**: Structured logging, error tracking, metrics

## Configuration Management

Environment-based configuration using Pydantic Settings:

1. Development: `.env` file
2. Production: Environment variables or secret management
3. Configuration validation at startup
4. Type-safe configuration access

## Next Steps

1. Implement remaining agent logic
2. Set up vector database for embeddings
3. Build out API endpoints
4. Create frontend components
5. Add comprehensive tests
6. Set up CI/CD pipeline
7. Deploy to production

For more details, see:
- [API Documentation](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
