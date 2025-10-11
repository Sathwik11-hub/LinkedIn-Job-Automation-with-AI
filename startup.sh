#!/bin/bash
# Startup script for AutoAgentHire
# Checks dependencies and starts all services

set -e

echo "🤖 AutoAgentHire - Starting services..."
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}✗ .env file not found${NC}"
    echo "  Creating from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your API keys before continuing${NC}"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated${NC}"
    echo "  Activate with: source venv/bin/activate"
    echo ""
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✓ PostgreSQL client found${NC}"
else
    echo -e "${YELLOW}⚠️  PostgreSQL client not found${NC}"
fi

# Check Redis
if command -v redis-cli &> /dev/null; then
    echo -e "${GREEN}✓ Redis CLI found${NC}"
else
    echo -e "${YELLOW}⚠️  Redis CLI not found${NC}"
fi

# Check Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker found${NC}"
    
    # Check if services are running
    if docker ps | grep -q postgres; then
        echo -e "${GREEN}✓ PostgreSQL container running${NC}"
    else
        echo -e "${YELLOW}⚠️  PostgreSQL container not running${NC}"
        echo "  Start with: docker-compose -f docker/docker-compose.yml up -d postgres"
    fi
    
    if docker ps | grep -q redis; then
        echo -e "${GREEN}✓ Redis container running${NC}"
    else
        echo -e "${YELLOW}⚠️  Redis container not running${NC}"
        echo "  Start with: docker-compose -f docker/docker-compose.yml up -d redis"
    fi
else
    echo -e "${YELLOW}⚠️  Docker not found${NC}"
fi

echo ""
echo "📚 Starting services..."
echo ""

# Function to start a service in background
start_service() {
    local name=$1
    local command=$2
    local port=$3
    
    echo "Starting $name on port $port..."
    $command &
    local pid=$!
    echo "$name PID: $pid"
}

# Parse command line arguments
case "${1:-all}" in
    backend)
        echo "🚀 Starting Backend API..."
        uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    
    frontend)
        echo "🎨 Starting Streamlit Frontend..."
        streamlit run frontend/streamlit/app.py --server.port 8501
        ;;
    
    docker)
        echo "🐳 Starting Docker services..."
        docker-compose -f docker/docker-compose.yml up
        ;;
    
    all)
        echo "🚀 Starting all services..."
        echo ""
        echo "Backend will be available at: http://localhost:8000"
        echo "API Docs will be available at: http://localhost:8000/docs"
        echo "Frontend will be available at: http://localhost:8501"
        echo ""
        echo "Press Ctrl+C to stop all services"
        echo ""
        
        # Start backend in background
        uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
        BACKEND_PID=$!
        
        # Give backend time to start
        sleep 3
        
        # Start frontend
        streamlit run frontend/streamlit/app.py --server.port 8501 &
        FRONTEND_PID=$!
        
        # Wait for both processes
        wait $BACKEND_PID $FRONTEND_PID
        ;;
    
    *)
        echo "Usage: ./startup.sh [backend|frontend|docker|all]"
        echo ""
        echo "Options:"
        echo "  backend  - Start FastAPI backend only"
        echo "  frontend - Start Streamlit frontend only"
        echo "  docker   - Start all services with Docker Compose"
        echo "  all      - Start backend and frontend (default)"
        exit 1
        ;;
esac
