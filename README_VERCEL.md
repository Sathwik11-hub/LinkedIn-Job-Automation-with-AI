# AutoAgentHire - Vercel Deployment

This is the serverless version of AutoAgentHire deployed on Vercel. It provides a demonstration of the API capabilities without browser automation features.

## 🌐 Live Demo

Visit the deployed application: [Your Vercel URL]

## 📚 API Endpoints

- **GET /** - Landing page with overview
- **GET /docs** - Interactive API documentation
- **GET /health** - Health check endpoint
- **GET /api/agent/status** - Agent configuration status
- **POST /api/run-agent** - Demo job analysis (mock results)
- **GET /api/demo** - Demo endpoint information

## 🔧 Features Available

### ✅ Available in Serverless
- PDF resume upload and validation
- Job search preference configuration
- AI-powered job compatibility analysis (when API keys configured)
- Mock job search results
- RESTful API with FastAPI
- Interactive API documentation

### ❌ Not Available (Requires Local Installation)
- Real LinkedIn browser automation
- Actual job applications
- Playwright/Selenium web scraping
- Streamlit UI (frontend)
- Extended timeout handling for slow connections

## 🚀 Local Installation

For the complete AutoAgentHire experience with browser automation:

```bash
git clone https://github.com/Sathwik11-hub/LinkedIn-Job-Automation-with-AI.git
cd LinkedIn-Job-Automation-with-AI
pip install -r requirements.txt
```

Follow the complete setup guide in the main repository.

## 🔑 Environment Variables

Set these in your Vercel dashboard for enhanced functionality:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 📝 Usage Example

```bash
# Health check
curl https://your-vercel-url.vercel.app/health

# Upload resume and get job analysis
curl -X POST https://your-vercel-url.vercel.app/api/run-agent \
  -F "file=@resume.pdf" \
  -F "keyword=AI Engineer" \
  -F "location=Remote" \
  -F "max_jobs=5"
```

## 🎯 Purpose

This serverless deployment demonstrates:
- FastAPI backend architecture
- File upload handling
- AI integration potential
- RESTful API design
- Error handling and validation

For production job automation, use the full local installation with browser capabilities.