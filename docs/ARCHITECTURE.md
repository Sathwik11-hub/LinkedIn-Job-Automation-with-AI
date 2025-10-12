# Architecture Documentation

## System Overview

AutoAgentHire is an autonomous AI agent system that automates job discovery and applications. The system uses a multi-agent architecture with LLMs, RAG, and web automation.

## High-Level Architecture

```
┌─────────────┐
│   Frontend  │ (Streamlit/React)
└──────┬──────┘
       │
       ├─── HTTP/WebSocket ───┐
       │                      │
┌──────▼──────────────────────▼──────┐
│         FastAPI Backend            │
│  ┌──────────────────────────────┐  │
│  │      API Layer               │  │
│  │  - Authentication            │  │
│  │  - Job Search Endpoints      │  │
│  │  - Application Endpoints     │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Agent Orchestrator      │  │
│  │  ┌────────────────────────┐  │  │
│  │  │  Job Search Agent      │  │  │
│  │  │  Analysis Agent        │  │  │
│  │  │  Application Agent     │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Core Services           │  │
│  │  - Resume Parser             │  │
│  │  - Job Matcher               │  │
│  │  - LLM Client                │  │
│  │  - Vector Store              │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Automation Layer        │  │
│  │  - Selenium/Playwright       │  │
│  │  - LinkedIn Scraper          │  │
│  │  - Form Filler               │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
       │              │            │
       │              │            │
   ┌───▼───┐    ┌────▼────┐  ┌───▼────┐
   │  DB   │    │ Vector  │  │  LLM   │
   │ (PG)  │    │  Store  │  │  API   │
   └───────┘    │(Chroma) │  │(OpenAI)│
                └─────────┘  └────────┘
```

## Components

### 1. Frontend Layer

**Streamlit Dashboard** (Simple UI)
- User-friendly interface for job search
- Resume upload and management
- Application tracking
- Analytics visualization

**React Dashboard** (Advanced UI)
- Modern, responsive interface
- Real-time updates via WebSocket
- Advanced filtering and search
- Interactive charts and analytics

### 2. API Layer (FastAPI)

**Authentication Module**
- JWT-based authentication
- OAuth2 integration (Google, LinkedIn)
- Role-based access control

**Job Endpoints**
- Job search and discovery
- Job detail retrieval
- Match analysis

**Application Endpoints**
- Application creation
- Status tracking
- Document management

**User Endpoints**
- Profile management
- Resume upload
- Preference configuration

### 3. Agent Layer (CrewAI/LangGraph)

**Job Search Agent**
- Role: Job Discovery Specialist
- Searches multiple job boards
- Extracts job details
- Stores in database

**Analysis Agent**
- Role: Job Fit Analyzer
- Calculates match scores
- Identifies strengths and gaps
- Ranks opportunities

**Application Agent**
- Role: Application Specialist
- Generates cover letters
- Fills application forms
- Manages submissions

**Orchestrator**
- Coordinates agent workflow
- Manages agent communication
- Handles error recovery

### 4. Core Services

**Resume Parser**
- PDF/DOCX/TXT support
- NER for information extraction
- Skill categorization
- Experience parsing

**Job Matcher**
- Semantic similarity (embeddings)
- Rule-based matching
- Hybrid scoring algorithm
- Recommendation engine

**LLM Integration**
- OpenAI GPT-4 client
- Prompt templates
- Token management
- Cost tracking

**Vector Store (RAG)**
- ChromaDB/Pinecone integration
- Document embeddings
- Semantic search
- Context retrieval

### 5. Automation Layer

**Web Automation**
- Selenium/Playwright drivers
- Anti-detection measures
- Cookie/session management

**LinkedIn Scraper**
- Job search automation
- Rate limiting
- CAPTCHA handling

**Form Filler**
- Field detection
- Auto-fill logic
- Multi-page support
- Human-in-the-loop

### 6. Data Layer

**PostgreSQL Database**
- Users and authentication
- Job listings
- Applications
- Match scores
- Encrypted credentials

**Vector Database (ChromaDB)**
- Resume embeddings
- Job description embeddings
- Semantic search indices

**Redis Cache**
- Session storage
- Task queue (Celery)
- Rate limiting

## Data Flow

### Job Search Workflow

1. **User initiates search**
   - Frontend sends search criteria to API
   - API validates and authenticates request

2. **Job Search Agent activates**
   - Searches multiple job boards
   - Extracts job details
   - Stores raw data in PostgreSQL

3. **Analysis Agent processes jobs**
   - Retrieves user resume from vector DB
   - Calculates match scores
   - Stores match results

4. **Results returned to user**
   - Ranked job list with match scores
   - Detailed match reasoning
   - Recommended actions

### Application Workflow

1. **User selects job to apply**
   - Frontend sends application request

2. **Application Agent activates**
   - Retrieves job details and user resume
   - Generates personalized cover letter using LLM
   - Prepares application data

3. **Form filling (optional)**
   - Selenium/Playwright navigates to application
   - Fills form fields automatically
   - Uploads resume and documents

4. **Human review**
   - User reviews generated content
   - Confirms or modifies application
   - Approves submission

5. **Submission and tracking**
   - Application submitted
   - Status tracked in database
   - Notification sent to user

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Agent Framework**: CrewAI / LangGraph
- **LLM**: OpenAI GPT-4
- **Database**: PostgreSQL (asyncpg)
- **Vector DB**: ChromaDB / Pinecone
- **Cache**: Redis
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

### Frontend
- **Streamlit**: Quick dashboard
- **React**: Advanced UI with Vite
- **Styling**: Tailwind CSS
- **State Management**: Context API / Zustand

### AI/ML
- **LangChain**: LLM orchestration
- **Sentence Transformers**: Embeddings
- **spaCy**: NLP and NER
- **PyPDF2**: PDF parsing

### Automation
- **Selenium**: Web automation
- **Playwright**: Modern automation
- **BeautifulSoup**: HTML parsing

### DevOps
- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **Nginx**: Reverse proxy

## Security Considerations

1. **Credential Encryption**
   - Fernet encryption for sensitive data
   - Environment-based key management
   - Audit logging

2. **Authentication**
   - JWT tokens with expiration
   - Refresh token rotation
   - OAuth2 integration

3. **Rate Limiting**
   - Per-user request limits
   - IP-based throttling
   - DDoS protection

4. **Data Privacy**
   - User data isolation
   - GDPR compliance
   - Secure file storage

## Scalability

1. **Horizontal Scaling**
   - Stateless API design
   - Load balancer (Nginx)
   - Database connection pooling

2. **Async Processing**
   - Celery for background tasks
   - Redis task queue
   - Scheduled jobs

3. **Caching Strategy**
   - Redis for session data
   - Response caching
   - Vector DB caching

## Monitoring & Observability

1. **Logging**
   - Structured logging (Loguru)
   - Log aggregation
   - Error tracking (Sentry)

2. **Metrics**
   - Prometheus metrics
   - API response times
   - Agent performance

3. **Alerts**
   - Failed applications
   - High error rates
   - API quota exceeded
