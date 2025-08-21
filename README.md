# AutoAgentHire - LinkedIn Job Automation with AI

🚀 **Intelligent LinkedIn Job Automation Platform**

AutoAgentHire is an AI-powered job automation platform that streamlines the job search and application process on LinkedIn. It combines web scraping, AI matching, and automated application submission to help job seekers efficiently apply to relevant positions.

## ✨ Features

### 🔍 **Smart Job Search**
- Automated LinkedIn job scraping with advanced filters
- Real-time job discovery based on keywords, location, and preferences
- Intelligent duplicate detection and job quality filtering

### 🧠 **AI-Powered Matching**
- Resume parsing using advanced NLP techniques
- AI-driven job-candidate matching with scoring algorithms
- Skill gap analysis and job recommendation engine
- Vector-based semantic similarity matching

### 📝 **Automated Cover Letter Generation**
- LLM-powered personalized cover letter creation
- Template-based fallback system
- Company and role-specific customization
- Quality scoring and optimization

### 🤖 **Intelligent Application Automation**
- Selenium-based LinkedIn automation
- Human-like interaction patterns to avoid detection
- Smart form filling and document upload
- Application tracking and status monitoring

### 📊 **Analytics & Insights**
- Application success rate tracking
- Match score analytics
- Performance monitoring and reporting
- Application history and insights

## 🏗️ Project Structure

```
AutoAgentHire/
│
├── app/                              # Main application folder
│   ├── __init__.py
│   ├── main.py                       # FastAPI entry point
│   ├── config.py                     # Environment variables & settings
│   ├── routes/                       # API routes
│   │   ├── __init__.py
│   │   └── jobs.py                   # Job search & apply endpoints
│   ├── services/                     # Business logic
│   │   ├── __init__.py
│   │   ├── job_scraper.py            # LinkedIn scraping logic
│   │   ├── resume_parser.py          # NLP resume parsing
│   │   ├── matcher.py                # AI matching & scoring
│   │   ├── cover_letter_generator.py # LLM-based cover letter creation
│   │   └── auto_apply.py             # Automation flow orchestration
│   ├── utils/                        # Helper utilities
│   │   ├── __init__.py
│   │   ├── logger.py                 # Logging utilities
│   │   └── vectorstore.py            # RAG embeddings & similarity
│   └── models/                       # Data models & schemas
│       ├── __init__.py
│       └── job_schema.py             # Pydantic models
│
├── automation/                       # Browser automation
│   ├── __init__.py
│   └── linkedin_bot.py               # LinkedIn automation bot
│
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── README.md                         # Project documentation
└── run.sh                            # Application startup script
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium automation)
- LinkedIn account
- OpenAI API key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI.git
   cd LinkedIn-Job-Automation-with-AI
   ```

2. **Run the setup script**
   ```bash
   ./run.sh
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your credentials
   ```

4. **Required environment variables:**
   ```env
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   OPENAI_API_KEY=your_openai_key  # Optional but recommended
   ```

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 API Documentation

Once the application is running, visit:
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Key Endpoints

#### Job Search
```http
POST /api/v1/jobs/search
```
Search for jobs with intelligent filtering and matching.

#### AI-Powered Job Matching
```http
POST /api/v1/jobs/match
```
Find and rank jobs based on resume compatibility.

#### Automated Application
```http
POST /api/v1/jobs/apply
```
Apply to a job with auto-generated cover letter.

#### Bulk Application
```http
POST /api/v1/jobs/bulk-apply
```
Apply to multiple jobs efficiently.

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LINKEDIN_EMAIL` | LinkedIn login email | Yes | - |
| `LINKEDIN_PASSWORD` | LinkedIn password | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key for AI features | No | - |
| `OPENAI_MODEL` | OpenAI model to use | No | gpt-3.5-turbo |
| `HEADLESS_BROWSER` | Run browser in headless mode | No | true |
| `MAX_APPLICATIONS_PER_DAY` | Daily application limit | No | 50 |
| `AUTOMATION_DELAY` | Delay between actions (seconds) | No | 2.0 |

### Advanced Configuration

The application supports extensive customization through the `app/config.py` file:

- **Database settings** (SQLite by default)
- **Vector store configuration** for AI matching
- **Logging levels and output**
- **Rate limiting and automation parameters**

## 🤖 Usage Examples

### Basic Job Search
```python
import requests

# Search for software engineer jobs
response = requests.post("http://localhost:8000/api/v1/jobs/search", json={
    "keywords": "software engineer",
    "location": "San Francisco, CA",
    "job_type": "full_time",
    "limit": 20
})

jobs = response.json()["jobs"]
```

### AI-Powered Matching
```python
# Match jobs against your resume
response = requests.post("http://localhost:8000/api/v1/jobs/match", json={
    "keywords": "data scientist",
    "location": "New York, NY",
    "resume_path": "/path/to/your/resume.pdf",
    "include_match_score": True
})

matched_jobs = response.json()
```

### Automated Application
```python
# Apply to a job automatically
response = requests.post("http://localhost:8000/api/v1/jobs/apply", json={
    "job_id": "linkedin_job_id",
    "resume_path": "/path/to/resume.pdf",
    "cover_letter_template": "standard"
})
```

## 🔒 Security & Best Practices

### Responsible Usage
- **Respect rate limits**: The application includes built-in delays and limits
- **Use responsibly**: Don't spam applications or violate LinkedIn's ToS
- **Secure credentials**: Never commit credentials to version control
- **Monitor usage**: Keep track of application activity and success rates

### Security Features
- Environment variable configuration for sensitive data
- Automatic rate limiting and human-like delays
- Session management and error handling
- Comprehensive logging for audit trails

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

For specific test categories:
```bash
# Test API endpoints
pytest tests/test_api/ -v

# Test AI matching
pytest tests/test_matching/ -v

# Test automation
pytest tests/test_automation/ -v
```

## 📈 Performance & Monitoring

### Built-in Analytics
- Application success/failure rates
- Average match scores
- Processing times and performance metrics
- Daily/weekly application summaries

### Monitoring
The application provides comprehensive logging and monitoring:
- Structured logging with different levels
- Performance tracking for AI operations
- Error tracking and debugging information
- Application status and health checks

## 🔧 Troubleshooting

### Common Issues

1. **LinkedIn Login Issues**
   - Verify credentials in `.env` file
   - Check for security challenges (may require manual intervention)
   - Ensure LinkedIn account is in good standing

2. **AI Features Not Working**
   - Verify OpenAI API key is valid
   - Check API usage limits and billing
   - Review model availability and permissions

3. **Browser Automation Issues**
   - Ensure Chrome browser is installed
   - Check if running in headless mode works
   - Verify ChromeDriver compatibility

4. **Resume Parsing Issues**
   - Ensure spaCy models are downloaded
   - Check resume file format (PDF, DOCX, TXT)
   - Verify file paths and permissions

### Debug Mode
Enable debug mode for detailed logging:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🚧 Development

### Setting up Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run code formatting
black app/ automation/ tests/
isort app/ automation/ tests/

# Run linting
flake8 app/ automation/ tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Respecting website rate limits and policies  
- Using the automation features responsibly
- Ensuring applications are relevant and appropriate

The developers are not responsible for any misuse of this tool or violations of platform policies.

## 🤝 Support

- **Documentation**: Check the `/docs` endpoint when running
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions for questions and support

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- Uses [Selenium](https://selenium.dev/) for browser automation
- Powered by [OpenAI](https://openai.com/) for AI features
- NLP processing with [spaCy](https://spacy.io/)
- Vector embeddings with [Sentence Transformers](https://www.sbert.net/)

---

**AutoAgentHire** - Revolutionizing job search with AI-powered automation 🚀