#!/bin/bash

# AutoAgentHire React Frontend Startup Script
echo "🚀 Starting AutoAgentHire React Frontend..."

# Navigate to the React frontend directory
cd "$(dirname "$0")"
REACT_DIR="./frontend/react"

# Check if we're in the right directory
if [ ! -d "$REACT_DIR" ]; then
    echo "❌ Error: React frontend directory not found at $REACT_DIR"
    exit 1
fi

cd "$REACT_DIR"

echo "🌐 Starting React development server on http://localhost:3000"
echo "📱 Frontend will connect to backend at http://127.0.0.1:8000"
echo ""
echo "✨ AutoAgentHire React Frontend is starting..."
echo "   - Modern React.js UI with Tailwind CSS"
echo "   - Real-time automation progress tracking"
echo "   - Beautiful glassmorphism design"
echo "   - Interactive job results display"
echo ""
npm run dev
# Ensure node/npm are available
if ! command -v node >/dev/null 2>&1; then
    echo "❌ Node.js is not installed or not in PATH."
    echo "Please install Node.js (LTS) from https://nodejs.org/ or via Homebrew:"
    echo "  /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  brew install node"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "❌ npm is not available. Please ensure Node.js/npm are installed correctly."
    exit 1
fi

cd "$REACT_DIR"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install || { echo "❌ npm install failed"; exit 1; }
fi

echo "🌐 Starting React development server on http://localhost:3000"
echo "📱 Frontend will connect to backend at http://127.0.0.1:8000"
echo ""
echo "✨ AutoAgentHire React Frontend is starting..."
echo "   - Modern React.js UI with Tailwind CSS"
echo "   - Real-time automation progress tracking"
echo "   - Beautiful glassmorphism design"
echo "   - Interactive job results display"
echo ""

npm run dev