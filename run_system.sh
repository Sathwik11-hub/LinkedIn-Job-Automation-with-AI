#!/bin/bash

# AutoAgentHire Startup Script
echo "🚀 Starting AutoAgentHire System..."

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "uvicorn\|streamlit" 2>/dev/null || true
sleep 2

# Activate virtual environment
source venv/bin/activate

# Find available ports
BACKEND_PORT=$(python -c "import socket; s = socket.socket(); s.bind(('', 0)); port = s.getsockname()[1]; s.close(); print(port)")
FRONTEND_PORT=$(python -c "import socket; s = socket.socket(); s.bind(('', 0)); port = s.getsockname()[1]; s.close(); print(port)")

echo "📡 Using backend port: $BACKEND_PORT"
echo "🖥️  Using frontend port: $FRONTEND_PORT"

# Update frontend configuration
sed -i "" "s|BACKEND_URL = \"http://127.0.0.1:[0-9]*\"|BACKEND_URL = \"http://127.0.0.1:$BACKEND_PORT\"|g" frontend/streamlit/autoagent_app.py

# Start backend in background
echo "🔧 Starting backend..."
python -m uvicorn backend.main:app --host 127.0.0.1 --port $BACKEND_PORT --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 5

# Test backend health
echo "🩺 Testing backend health..."
if curl -s "http://127.0.0.1:$BACKEND_PORT/health" > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "Backend logs:"
    tail -n 20 backend.log
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend..."
streamlit run frontend/streamlit/autoagent_app.py --server.port $FRONTEND_PORT --server.headless false

# Clean up on exit
trap "echo '🛑 Shutting down...'; kill $BACKEND_PID 2>/dev/null || true; pkill -f 'uvicorn\|streamlit' 2>/dev/null || true" EXIT