#!/bin/bash

# AutoAgentHire - LinkedIn Job Automation with AI
# Run script for starting the application

set -e

echo "🚀 Starting AutoAgentHire - LinkedIn Job Automation with AI"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model if not exists
echo "🧠 Setting up NLP models..."
python -m spacy download en_core_web_sm || echo "spaCy model already installed or download failed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your credentials before running the application"
    echo "🔑 Required: LINKEDIN_EMAIL, LINKEDIN_PASSWORD, OPENAI_API_KEY"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p vector_store
mkdir -p logs
mkdir -p uploads/resumes
mkdir -p uploads/cover_letters

# Check environment variables
echo "🔍 Checking environment configuration..."
if [ -f ".env" ]; then
    source .env
    
    if [ -z "$LINKEDIN_EMAIL" ] || [ -z "$LINKEDIN_PASSWORD" ]; then
        echo "⚠️  WARNING: LinkedIn credentials not set in .env file"
        echo "   Application will run but automation features will be limited"
    fi
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  WARNING: OpenAI API key not set in .env file"
        echo "   AI features will use fallback templates"
    fi
fi

# Start the application
echo "🏃 Starting AutoAgentHire application..."
echo "📡 API will be available at: http://localhost:${PORT:-8000}"
echo "📖 API documentation at: http://localhost:${PORT:-8000}/docs"
echo "🛑 Press Ctrl+C to stop the application"

# Run with uvicorn
python -m uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --reload

echo "👋 AutoAgentHire stopped"