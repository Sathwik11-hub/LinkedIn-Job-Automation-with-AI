#!/bin/bash

# AutoAgentHire - Complete Setup and Run Script

echo "🤖 AutoAgentHire - AI-Powered LinkedIn Job Automation"
echo "======================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Creating .env from template..."
    
    cat > .env << 'EOF'
# LinkedIn Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key

# User Information (for auto-fill)
FIRST_NAME=John
LAST_NAME=Doe
PHONE_NUMBER=+1234567890
LINKEDIN_URL=https://linkedin.com/in/yourprofile
PORTFOLIO_URL=https://yourportfolio.com

# Application Settings
MAX_APPLICATIONS=5
SIMILARITY_THRESHOLD=0.6
AUTO_APPLY=true
HEADLESS_MODE=false

# Server Settings
API_HOST=127.0.0.1
API_PORT=50501
EOF
    
    echo -e "${YELLOW}⚠️  Please edit .env file with your credentials${NC}"
    echo "Then run this script again."
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}❌ Python 3.9+ required. Found: $PYTHON_VERSION${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --quiet --upgrade pip

# Install required packages
pip install --quiet \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    playwright==1.40.0 \
    python-multipart==0.0.6 \
    python-dotenv==1.0.0 \
    google-generativeai==0.8.5 \
    pydantic==2.5.0 \
    PyPDF2==3.0.1 \
    aiofiles==23.2.1

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium --with-deps
echo -e "${GREEN}✅ Playwright browsers installed${NC}"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads/resumes
mkdir -p uploads/cover_letters
mkdir -p reports
mkdir -p logs
echo -e "${GREEN}✅ Directories created${NC}"

# Check .env configuration
echo ""
echo "🔍 Checking configuration..."

source .env

if [[ "$LINKEDIN_EMAIL" == "your_email@example.com" ]]; then
    echo -e "${RED}❌ LinkedIn email not configured${NC}"
    CONFIG_OK=false
else
    echo -e "${GREEN}✅ LinkedIn email: $LINKEDIN_EMAIL${NC}"
    CONFIG_OK=true
fi

if [[ "$LINKEDIN_PASSWORD" == "your_password" ]]; then
    echo -e "${RED}❌ LinkedIn password not configured${NC}"
    CONFIG_OK=false
else
    echo -e "${GREEN}✅ LinkedIn password: [HIDDEN]${NC}"
fi

if [[ "$GEMINI_API_KEY" == "your_gemini_api_key" ]]; then
    echo -e "${YELLOW}⚠️  Gemini API not configured (will use fallback matching)${NC}"
else
    echo -e "${GREEN}✅ Gemini API key: ${GEMINI_API_KEY:0:10}...${NC}"
fi

if [ "$CONFIG_OK" = false ]; then
    echo ""
    echo -e "${RED}❌ Configuration incomplete. Please update .env file.${NC}"
    exit 1
fi

# Start the backend server
echo ""
echo "🚀 Starting AutoAgentHire backend..."
echo "======================================================"
echo ""
echo -e "${GREEN}Backend API: http://127.0.0.1:50501${NC}"
echo -e "${GREEN}API Docs: http://127.0.0.1:50501/docs${NC}"
echo -e "${GREEN}Frontend UI: Open frontend/autoagenthire/index.html in browser${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Run the FastAPI server
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 50501 --reload
