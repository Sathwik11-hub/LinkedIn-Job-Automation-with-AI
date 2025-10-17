#!/bin/bash

# AutoAgentHire Backend Startup Script
echo "🚀 Starting AutoAgentHire Backend..."

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start backend server
echo "📡 Starting FastAPI server on http://127.0.0.1:50501"
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 50501 --reload
