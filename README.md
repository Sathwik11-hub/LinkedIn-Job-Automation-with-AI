# AutoAgentHire: AI-Powered LinkedIn Job Application Automation

![AutoAgentHire](https://img.shields.io/badge/AutoAgentHire-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-green.svg)
![React](https://img.shields.io/badge/React-18+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red.svg)

**AutoAgentHire** is an intelligent, AI-powered system that automates LinkedIn job applications using modern web automation, machine learning, and natural language processing. The system intelligently matches your skills with job requirements, generates personalized cover letters, and applies to jobs automatically while maintaining professional standards.

## 🏗 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AutoAgentHire System                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React/TypeScript)                               │
│  ├── User Dashboard                                        │
│  ├── Job Preferences Setup                                 │
│  ├── Application Status Tracker                            │
│  └── Reports & Analytics                                   │
├─────────────────────────────────────────────────────────────┤
│  Backend API (FastAPI)                                     │
│  ├── Authentication Service                                │
│  ├── Job Search Orchestrator                              │
│  ├── Application Manager                                   │
│  └── Reporting Service                                     │
├─────────────────────────────────────────────────────────────┤
│  AI Engine Layer                                          │
│  ├── LLM Integration (OpenAI)                             │
│  ├── Resume Parser                                        │
│  ├── Job Matching Algorithm                               │
│  └── Cover Letter Generator                               │
├─────────────────────────────────────────────────────────────┤
│  Automation Layer                                         │
│  ├── LinkedIn Bot (Playwright)                            │
│  ├── Form Filler                                          │
│  └── Application Tracker                                  │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                               │
│  ├── PostgreSQL (User Data, Applications)                 │
│  ├── Redis Cache (Session Management)                     │
│  └── File Storage (Resumes, Cover Letters)               │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Features

### 🤖 AI-Powered Automation
- **Intelligent Job Matching**: AI analyzes job descriptions and matches them with your skills
- **Personalized Cover Letters**: GPT-powered cover letter generation tailored to each job
- **Resume Parsing**: Automatic extraction of skills, experience, and education from PDF resumes
- **Smart Application Strategy**: Prioritizes applications based on compatibility scores

### 🎯 LinkedIn Integration
- **Automated Job Search**: Searches LinkedIn jobs based on your preferences
- **Easy Apply Automation**: Automatically applies to jobs with "Easy Apply" feature
- **Application Tracking**: Monitors application status and responses
- **Rate Limiting**: Respects LinkedIn's terms of service with intelligent delays

### 📊 Analytics & Reporting
- **Real-time Dashboard**: Track applications, success rates, and trends
- **Detailed Analytics**: Insights into application patterns and performance
- **Success Metrics**: Monitor interview callbacks and job offers
- **Export Capabilities**: Generate reports in multiple formats

### 🔒 Security & Compliance
- **Secure Authentication**: JWT-based user authentication
- **Encrypted Credentials**: Secure storage of LinkedIn credentials
- **GDPR Compliant**: Respects user privacy and data protection
- **Ethical Automation**: Follows LinkedIn's terms of service

## 🛠 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL**: Robust relational database
- **Redis**: In-memory data structure store for caching
- **Celery**: Distributed task queue

### AI & ML
- **OpenAI GPT**: Large language model for text generation
- **LangChain**: Framework for developing LLM applications
- **spaCy**: Industrial-strength NLP library
- **PyPDF2**: PDF text extraction
- **FAISS**: Vector similarity search

### Automation
- **Playwright**: Modern web automation framework
- **Selenium**: Web browser automation (fallback)
- **BeautifulSoup**: HTML parsing and scraping

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **TypeScript**: Typed superset of JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API requests
- **React Router**: Declarative routing for React

### DevOps
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container Docker applications
- **PostgreSQL**: Database containerization
- **Redis**: Cache containerization

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (if running locally)
- OpenAI API key

### 1. Clone the Repository
```bash
git clone https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI.git
cd LinkedIn-Job-Automation-with-AI
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

### 3. Docker Setup (Recommended)
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Manual Setup (Alternative)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/autoagenthire
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your_openai_api_key_here

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LinkedIn Credentials (for automation)
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Application Settings
DEBUG=True
ENVIRONMENT=development
HEADLESS_BROWSER=True
```

## 📖 Usage Guide

### 1. Initial Setup
1. **Register an Account**: Create your user account
2. **Upload Resume**: Upload your PDF resume for parsing
3. **Set Preferences**: Configure job search parameters
4. **LinkedIn Credentials**: Securely store LinkedIn login details

### 2. Job Search & Applications
1. **Search Jobs**: Use the job search feature to find relevant positions
2. **Review Matches**: Check AI-generated compatibility scores
3. **Batch Apply**: Select multiple jobs for automated application
4. **Monitor Progress**: Track applications in real-time

### 3. Analytics & Optimization
1. **Dashboard**: Monitor key metrics and success rates
2. **Reports**: Generate detailed analytics reports
3. **Optimize Strategy**: Adjust preferences based on performance
4. **Export Data**: Download application data for external analysis

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Run full integration test suite
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📁 Project Structure

```
autoagenthire/
├── 📁 backend/                 # FastAPI backend application
│   ├── 📁 app/
│   │   ├── 📁 api/v1/          # API route handlers
│   │   ├── 📁 core/            # Core configuration and database
│   │   ├── 📁 models/          # SQLAlchemy models
│   │   ├── 📁 schemas/         # Pydantic schemas
│   │   ├── 📁 services/        # Business logic services
│   │   │   ├── 📁 ai/          # AI and ML services
│   │   │   └── 📁 automation/  # Web automation services
│   │   └── main.py             # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend Docker configuration
├── 📁 frontend/                # React frontend application
│   ├── 📁 src/
│   │   ├── 📁 components/      # React components
│   │   ├── 📁 services/        # API service layer
│   │   └── App.tsx             # Main application component
│   ├── package.json            # Node.js dependencies
│   └── Dockerfile              # Frontend Docker configuration
├── 📁 data/                    # Data storage
│   ├── 📁 resumes/            # User resume files
│   ├── 📁 cover_letters/      # Generated cover letters
│   └── 📁 job_data/           # Scraped job data
├── 📁 ai_models/              # AI model storage
│   ├── 📁 embeddings/         # Vector embeddings
│   └── 📁 prompts/            # LLM prompts
├── docker-compose.yml          # Multi-container setup
├── .env.example               # Environment variables template
└── README.md                  # Project documentation
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Add tests for new features
- Update documentation as needed
- Ensure Docker builds successfully

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This tool is designed to assist with job applications while respecting LinkedIn's terms of service. Users are responsible for:
- Ensuring compliance with LinkedIn's automation policies
- Using the tool ethically and responsibly
- Monitoring their account for any issues
- Respecting rate limits and platform guidelines

The developers are not responsible for any account restrictions or violations that may result from improper use.

## 🆘 Support

- **Documentation**: Check our [Wiki](https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI/wiki)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI/discussions)

## 🙏 Acknowledgments

- OpenAI for powerful language models
- LinkedIn for the platform (used respectfully)
- The open-source community for amazing tools and libraries
- Contributors who help improve this project

---

**Built with ❤️ by the AutoAgentHire Team**