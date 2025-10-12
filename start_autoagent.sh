#!/bin/bash

# AutoAgentHire - Enhanced Startup Script with AutoAgent Default
echo "🚀 AutoAgentHire - LinkedIn Job Automation System"
echo "✨ Enhanced with AutoAgent as Default Behavior"
echo ""

# Clean up any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn\|streamlit" 2>/dev/null || true
sleep 2

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q fastapi uvicorn streamlit pandas numpy requests python-dotenv aiofiles google-generativeai playwright

# Install playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install

# Initialize database
echo "🗄️ Initializing database..."
PYTHONPATH=. python scripts/setup_db.py

# Check configuration
echo "⚙️ Checking configuration..."
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys and credentials"
fi

# Start backend
echo "🔧 Starting AutoAgentHire backend..."
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Test backend health
echo "🩺 Testing backend health..."
if curl -s "http://localhost:8000/health" > /dev/null; then
    echo "✅ Backend is healthy and ready"
else
    echo "❌ Backend health check failed"
    echo "📋 Backend logs:"
    tail -n 10 backend.log
    exit 1
fi

# Start frontend
echo "🎨 Starting enhanced frontend with AutoAgent..."
streamlit run frontend/streamlit/autoagent_app.py --server.port 8501 --server.headless false > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
sleep 3

echo ""
echo "🎉 AutoAgentHire is now running with AutoAgent as default!"
echo ""
echo "📍 Access Points:"
echo "   🌐 Frontend:     http://localhost:8501"
echo "   🔌 Backend API:  http://localhost:8000"
echo "   📚 API Docs:     http://localhost:8000/docs"
echo ""
echo "🤖 AutoAgent Features:"
echo "   ✨ Quick Start button for instant job automation"
echo "   🎯 Smart job matching with AI analysis"
echo "   📝 Automatic LinkedIn Easy Apply submissions"
echo "   📊 Real-time progress tracking and analytics"
echo ""
echo "⚙️ Configuration:"
echo "   📝 Update .env with your LinkedIn credentials"
echo "   🔑 Add your GEMINI_API_KEY for AI features"
echo "   📄 Upload your resume or use the default one"
echo ""
echo "🛑 To stop: Press Ctrl+C or run: pkill -f \"uvicorn\\|streamlit\""
echo ""

# Open browser (macOS)
if command -v open &> /dev/null; then
    echo "🌐 Opening frontend in browser..."
    sleep 2
    open http://localhost:8501
fi

# Keep script running and monitor processes
trap "echo '🛑 Shutting down AutoAgentHire...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; pkill -f 'uvicorn\\|streamlit' 2>/dev/null || true; exit 0" INT TERM

echo "✅ System is running. Press Ctrl+C to stop."
echo "📊 Monitoring processes..."

# Monitor loop
while true; do
    if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "⚠️  Backend process stopped unexpectedly"
        break
    fi
    if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "⚠️  Frontend process stopped unexpectedly"
        break
    fi
    sleep 10
done

# Cleanup on exit
echo "🧹 Cleaning up..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
pkill -f 'uvicorn\|streamlit' 2>/dev/null || true
echo "👋 AutoAgentHire stopped."