#!/bin/bash
# Quick setup script for AutoAgentHire

set -e

echo "🚀 Setting up AutoAgentHire..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file if not exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys and configuration"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/logs data/resumes data/job_listings vector_db/data

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
    echo "💡 You can run 'docker-compose -f docker/docker-compose.yml up' to start services"
else
    echo "⚠️  Docker is not installed. Install Docker to use containerized deployment."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys: nano .env"
echo "2. Start PostgreSQL and Redis (via Docker or locally)"
echo "3. Initialize database: python scripts/setup_db.py"
echo "4. Run backend: uvicorn backend.main:app --reload"
echo "5. Run frontend: streamlit run frontend/streamlit/app.py"
echo ""
echo "📚 Documentation:"
echo "- API Docs: docs/API.md"
echo "- Architecture: docs/ARCHITECTURE.md"
echo "- Deployment: docs/DEPLOYMENT.md"
