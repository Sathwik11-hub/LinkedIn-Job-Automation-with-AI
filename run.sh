#!/bin/bash

# Simple startup script for AutoAgentHire

echo "🤖 Starting AutoAgentHire..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "Please edit .env and add your GOOGLE_API_KEY"
    echo ""
fi

# Create directories
mkdir -p uploads/resumes uploads/cover_letters logs vector_store data/job_listings

# Kill existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:8501 | xargs kill -9 2>/dev/null || true

echo "Starting Backend API on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload > logs/backend.log 2>&1 &

sleep 3

echo "Starting Frontend UI on port 8501..."
streamlit run frontend/streamlit/app_enhanced.py --server.port 8501 > logs/frontend.log 2>&1 &

sleep 2

echo ""
echo "========================================="
echo "✅ AutoAgentHire is running!"
echo "========================================="
echo ""
echo "📱 Frontend:    http://localhost:8501"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs:    http://localhost:8000/docs"
echo ""
echo "📋 View logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "Press Ctrl+C to stop (or run: killall -9 uvicorn streamlit)"
echo ""

# Keep script running
wait
