# AutoAgentHire - LinkedIn Job Automation with AI

🚀 **AutoAgentHire** is a comprehensive AI-powered system that automates LinkedIn job searching and application processes using advanced technologies like Retrieval-Augmented Generation (RAG), Natural Language Processing, and intelligent automation.

## 🌟 Features

### 🔍 Intelligent Job Search
- **LinkedIn Integration**: Automated job scraping with advanced filters
- **Smart Filtering**: Filter by role, location, experience level, salary, and more
- **Real-time Data**: Fresh job postings with detailed information extraction

### 📄 Resume Intelligence
- **PDF Parsing**: Extract skills, experience, and education from resume PDFs
- **NLP Processing**: Advanced text analysis using spaCy
- **Structured Data**: Convert unstructured resume content to structured format

### 🎯 AI-Powered Job Matching
- **RAG Technology**: Vector-based job matching using FAISS/Chroma
- **Semantic Search**: Find relevant jobs beyond keyword matching
- **Similarity Scoring**: Calculate compatibility scores between jobs and resume
- **Smart Recommendations**: AI-driven job application recommendations

### ✍️ Personalized Cover Letters
- **LLM Integration**: Generate cover letters using OpenAI GPT or LLaMA
- **Personalization**: Tailored content based on job requirements and resume
- **Multiple Variants**: Generate different cover letter styles for A/B testing
- **Quality Scoring**: Automatic assessment of cover letter personalization

### 🤖 Application Automation
- **Easy Apply**: Automated application submission via LinkedIn's Easy Apply
- **Form Filling**: Intelligent form completion with resume data
- **Rate Limiting**: Respects LinkedIn's usage policies with delays
- **Error Handling**: Robust error handling and recovery mechanisms

### 📊 Analytics & Logging
- **Application Tracking**: Monitor application status and outcomes
- **Performance Metrics**: Track success rates and response times
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Statistics Dashboard**: Visual insights into job search performance

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Automation**: Selenium WebDriver for browser automation
- **AI/ML**: 
  - OpenAI GPT for cover letter generation
  - LLaMA 3 support for local LLM deployment
  - spaCy for NLP and resume parsing
  - Sentence Transformers for embeddings
- **Vector Database**: FAISS or ChromaDB for RAG implementation
- **Document Processing**: PyMuPDF for PDF parsing
- **Data Processing**: Pandas, NumPy for data manipulation
- **Environment**: python-dotenv for configuration management

## 📁 Project Structure

```
AutoAgentHire/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   └── logging.py         # Logging setup
│   ├── models/
│   │   └── __init__.py        # Pydantic data models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── linkedin_scraper.py      # LinkedIn scraping service
│   │   ├── resume_parser.py         # Resume parsing service
│   │   ├── job_matching.py          # RAG-based job matching
│   │   ├── cover_letter_generator.py # AI cover letter generation
│   │   └── application_automator.py  # Application automation
│   ├── utils/
│   │   └── __init__.py        # Utility functions
│   └── __init__.py
├── tests/                     # Test suite
├── data/
│   ├── resumes/              # Resume storage
│   └── jobs/                 # Job data and vector database
├── logs/                     # Application logs
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
├── .env.template            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- LinkedIn account
- OpenAI API key (optional, for advanced cover letter generation)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/AutoAgentHire.git
cd AutoAgentHire

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

### 3. Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your credentials
nano .env
```

**Required Environment Variables:**
```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# OpenAI API (optional)
OPENAI_API_KEY=your_openai_api_key

# Application Settings
SECRET_KEY=your_secret_key_change_this
```

### 4. Run the Application

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Interactive API Docs
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### 📤 Resume Management
```http
POST /upload-resume
Content-Type: multipart/form-data

# Upload and parse resume PDF
```

#### 🔍 Job Search
```http
POST /search-jobs
Content-Type: application/json

{
  "keywords": "Python Developer",
  "location": "Remote",
  "experience_level": "Mid-Senior level",
  "max_results": 50
}
```

#### 🎯 Job Matching
```http
POST /match-jobs
Content-Type: application/json

{
  "top_k": 20
}
```

#### ✍️ Cover Letter Generation
```http
POST /generate-cover-letters
Content-Type: application/json

{
  "job_ids": ["job123", "job456"],
  "custom_template": "Focus on technical achievements"
}
```

#### 🤖 Auto Apply
```http
POST /auto-apply
Content-Type: application/json

{
  "job_ids": ["job123", "job456"],
  "min_similarity_score": 0.7,
  "dry_run": true
}
```

## 💡 Usage Examples

### Basic Workflow

1. **Upload Resume**
```python
import requests

# Upload resume
with open("resume.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload-resume",
        files={"file": f}
    )
```

2. **Search Jobs**
```python
# Search for Python developer jobs
search_data = {
    "keywords": "Python Developer",
    "location": "San Francisco",
    "experience_level": "Mid-Senior level",
    "remote_only": True,
    "max_results": 20
}

response = requests.post(
    "http://localhost:8000/search-jobs",
    json=search_data
)
jobs = response.json()
```

3. **Match Jobs**
```python
# Get job matches
response = requests.post(
    "http://localhost:8000/match-jobs",
    json={"top_k": 10}
)
matches = response.json()
```

4. **Apply to Jobs**
```python
# Auto-apply to top matches
job_ids = [match["job_id"] for match in matches["matches"][:5]]

apply_request = {
    "job_ids": job_ids,
    "min_similarity_score": 0.8,
    "dry_run": False  # Set to True for testing
}

response = requests.post(
    "http://localhost:8000/auto-apply",
    json=apply_request
)
```

## ⚠️ Important Considerations

### Legal and Ethical Usage
- **Respect LinkedIn's Terms of Service**: Use responsibly and within rate limits
- **Employment Laws**: Ensure compliance with local employment and privacy laws
- **Data Privacy**: Handle personal data securely and transparently

### Rate Limiting
- Built-in delays between applications (configurable)
- Daily application limits to prevent account suspension
- Exponential backoff for error handling

### Security Best Practices
- Store credentials securely using environment variables
- Use strong, unique passwords for LinkedIn accounts
- Regularly rotate API keys and passwords
- Monitor for suspicious account activity

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/test_resume_parser.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## 📊 Monitoring and Logging

### Log Files
- **Application logs**: `logs/autoagenthire.log`
- **Error logs**: `logs/errors.log`

### Log Levels
```python
# Configure in .env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### Statistics Endpoint
```http
GET /stats

# Returns system statistics including:
# - Resume status
# - Cached jobs count
# - Vector database statistics
# - Application success rates
```

## 🔧 Configuration Options

### Job Search Settings
```env
DEFAULT_LOCATION=Remote
DEFAULT_EXPERIENCE_LEVEL=Mid-Senior level
MAX_APPLICATIONS_PER_DAY=50
APPLICATION_DELAY_SECONDS=30
```

### Vector Database
```env
VECTOR_DB_TYPE=faiss  # or chroma
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### File Paths
```env
RESUME_PATH=./data/resumes/
LOGS_PATH=./logs/
JOBS_DATA_PATH=./data/jobs/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/
flake8 src/

# Run type checking
mypy src/
```

## 🐛 Troubleshooting

### Common Issues

1. **LinkedIn Login Fails**
   - Check credentials in `.env` file
   - Ensure 2FA is disabled or handle it manually
   - Verify account is not suspended

2. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Chrome Driver Issues**
   - Update Chrome browser
   - Clear browser cache and data
   - Check firewall/antivirus settings

4. **OpenAI API Errors**
   - Verify API key is valid
   - Check API usage limits
   - Ensure sufficient credits

### Debug Mode
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Following local employment laws and regulations
- Using the tool ethically and responsibly
- Ensuring data privacy and security

The developers are not responsible for any account suspensions, legal issues, or misuse of this software.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Selenium](https://selenium.dev/) for browser automation capabilities
- [spaCy](https://spacy.io/) for natural language processing
- [OpenAI](https://openai.com/) for GPT API
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector similarity search

---

**⭐ If you find this project helpful, please give it a star on GitHub!**