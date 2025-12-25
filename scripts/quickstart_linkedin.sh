#!/bin/bash
# Quick Start Script for LinkedIn Auto Apply
# This script helps you get started quickly with the automation

echo "🤖 LinkedIn Auto Apply - Quick Start"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
playwright install chromium

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your credentials!"
    echo "   - LINKEDIN_EMAIL"
    echo "   - LINKEDIN_PASSWORD"
    echo "   - RESUME_PATH"
    echo ""
    echo "Then run: python linkedin_auto_apply.py"
    exit 0
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/resumes
mkdir -p reports
mkdir -p logs

# Check if resume exists
RESUME_PATH=$(grep RESUME_PATH .env | cut -d '=' -f2)
if [ ! -f "$RESUME_PATH" ]; then
    echo "⚠️  Warning: Resume not found at $RESUME_PATH"
    echo "   Please place your resume (PDF or TXT) at the specified path"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Quick Commands:"
echo "   python linkedin_auto_apply.py           # Run automation"
echo "   python linkedin_auto_apply.py --help    # Show help"
echo "   tail -f linkedin_automation.log         # View logs"
echo ""
echo "🚀 Ready to start? Run:"
echo "   python linkedin_auto_apply.py"
echo ""
