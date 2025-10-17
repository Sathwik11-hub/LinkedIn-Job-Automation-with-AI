#!/bin/bash

# 🚀 AutoAgentHire - One-Command Startup
# This script starts the complete system with health checks

echo "🤖 ======================================"
echo "   AutoAgentHire - Starting System"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check Python
echo -e "${BLUE}[1/6]${NC} Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python found${NC}"

# Check/Create virtual environment
echo -e "${BLUE}[2/6]${NC} Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi
echo -e "${GREEN}✓ Virtual environment ready${NC}"

# Activate venv
source venv/bin/activate

# Install/Update dependencies
echo -e "${BLUE}[3/6]${NC} Installing dependencies..."
pip install -q --upgrade pip
if pip install -q -r requirements.txt; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Dependency installation failed${NC}"
    exit 1
fi

# Check .env
echo -e "${BLUE}[4/6]${NC} Checking configuration..."
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your GOOGLE_API_KEY${NC}"
    echo "Press Enter when ready..."
    read
fi
echo -e "${GREEN}✓ Configuration file exists${NC}"

# Create directories
echo -e "${BLUE}[5/6]${NC} Creating directories..."
mkdir -p uploads/resumes uploads/cover_letters logs vector_store data/job_listings
echo -e "${GREEN}✓ Directories created${NC}"

# Kill existing processes on ports
echo -e "${BLUE}[6/6]${NC} Checking ports..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}Killing process on port 8000...${NC}"
    kill -9 $(lsof -t -i:8000) 2>/dev/null || true
    sleep 1
fi

if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}Killing process on port 8501...${NC}"
    kill -9 $(lsof -t -i:8501) 2>/dev/null || true
    sleep 1
fi
echo -e "${GREEN}✓ Ports available${NC}"

echo ""
echo "========================================="
echo -e "${GREEN}   Starting Services...${NC}"
echo "========================================="
echo ""

# Start backend
echo -e "${BLUE}Starting Backend API...${NC}"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend
echo -n "Waiting for backend"
for i in {1..15}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo ""
        echo -e "${GREEN}✓ Backend is running!${NC}"
        break
    fi
    echo -n "."
    sleep 1
    if [ $i -eq 15 ]; then
        echo ""
        echo -e "${RED}✗ Backend failed to start${NC}"
        echo "Check logs/backend.log for details"
        exit 1
    fi
done

# Start frontend
echo -e "${BLUE}Starting Frontend UI...${NC}"
streamlit run frontend/streamlit/app_enhanced.py --server.port 8501 --server.headless true > logs/frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 3

echo ""
echo "========================================="
echo -e "${GREEN}   ✓ AutoAgentHire is Running!${NC}"
echo "========================================="
echo ""
echo -e "${BLUE}📱 Frontend UI:${NC}    http://localhost:8501"
echo -e "${BLUE}🔧 Backend API:${NC}    http://localhost:8000"
echo -e "${BLUE}📖 API Docs:${NC}       http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}📋 View Logs:${NC}"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo -e "${YELLOW}🛑 Stop Services:${NC}"
echo "   Press Ctrl+C"
echo ""
echo "========================================="
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down AutoAgentHire...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✓ Services stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep running
wait
