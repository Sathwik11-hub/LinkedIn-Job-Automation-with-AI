#!/bin/bash

# AutoAgentHire Development Setup Script

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main setup function
main() {
    echo -e "${GREEN}"
    cat << "EOF"
    ░█████╗░██╗░░░██╗████████╗░█████╗░░█████╗░░██████╗░███████╗███╗░░██╗████████╗██╗░░██╗██╗██████╗░███████╗
    ██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗██╔══██╗██╔════╝░██╔════╝████╗░██║╚══██╔══╝██║░░██║██║██╔══██╗██╔════╝
    ███████║██║░░░██║░░░██║░░░██║░░██║███████║██║░░██╗░█████╗░░██╔██╗██║░░░██║░░░███████║██║██████╔╝█████╗░░
    ██╔══██║██║░░░██║░░░██║░░░██║░░██║██╔══██║██║░░╚██╗██╔══╝░░██║╚████║░░░██║░░░██╔══██║██║██╔══██╗██╔══╝░░
    ██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝██║░░██║╚██████╔╝███████╗██║░╚███║░░░██║░░░██║░░██║██║██║░░██║███████╗
    ╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝╚══════╝
    
    AI-Powered LinkedIn Job Application Automation System
    
EOF
    echo -e "${NC}"
    
    print_status "Starting AutoAgentHire development setup..."
    
    # Check system requirements
    check_requirements
    
    # Setup environment
    setup_environment
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Final instructions
    print_final_instructions
}

check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python 3 found: $PYTHON_VERSION"
    else
        print_error "Python 3 is required but not found. Please install Python 3.9+"
        exit 1
    fi
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_success "Node.js found: $NODE_VERSION"
    else
        print_error "Node.js is required but not found. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_success "npm found: $NPM_VERSION"
    else
        print_error "npm is required but not found."
        exit 1
    fi
    
    # Check Docker (optional)
    if command_exists docker; then
        print_success "Docker found"
    else
        print_warning "Docker not found. Docker is optional but recommended for development."
    fi
    
    # Check git
    if command_exists git; then
        print_success "Git found"
    else
        print_error "Git is required but not found."
        exit 1
    fi
}

setup_environment() {
    print_status "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your actual API keys and credentials"
    else
        print_success ".env file already exists"
    fi
    
    # Create necessary directories
    print_status "Creating data directories..."
    mkdir -p data/resumes data/cover_letters data/job_data
    mkdir -p ai_models/embeddings ai_models/vector_stores
    mkdir -p logs
    
    print_success "Environment setup complete"
}

setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_success "Backend setup complete"
    cd ..
}

setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    print_success "Frontend setup complete"
    cd ..
}

print_final_instructions() {
    echo
    print_success "🎉 AutoAgentHire setup complete!"
    echo
    print_status "Next steps:"
    echo
    echo "1. Configure your environment:"
    echo "   - Edit .env file with your API keys (OpenAI, LinkedIn credentials)"
    echo "   - Ensure PostgreSQL is running (or use Docker)"
    echo
    echo "2. Start the services:"
    echo
    echo "   Option A - Using Docker (Recommended):"
    echo "   ${GREEN}docker-compose up -d${NC}"
    echo
    echo "   Option B - Manual setup:"
    echo "   ${GREEN}# Terminal 1 - Start backend${NC}"
    echo "   ${GREEN}cd backend && source venv/bin/activate && uvicorn app.main:app --reload${NC}"
    echo
    echo "   ${GREEN}# Terminal 2 - Start frontend${NC}"
    echo "   ${GREEN}cd frontend && npm start${NC}"
    echo
    echo "3. Access the application:"
    echo "   - Frontend: ${BLUE}http://localhost:3000${NC}"
    echo "   - Backend API: ${BLUE}http://localhost:8000${NC}"
    echo "   - API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo
    echo "4. Setup database (if not using Docker):"
    echo "   ${GREEN}python scripts/setup_db.py --sample-data${NC}"
    echo
    print_warning "Don't forget to:"
    echo "   - Add your OpenAI API key to .env"
    echo "   - Configure LinkedIn credentials for automation"
    echo "   - Review security settings before production use"
    echo
}

# Parse command line arguments
case "${1:-setup}" in
    "setup")
        main
        ;;
    "backend-only")
        check_requirements
        setup_environment
        setup_backend
        ;;
    "frontend-only")
        check_requirements
        setup_frontend
        ;;
    "help"|"-h"|"--help")
        echo "AutoAgentHire Development Setup"
        echo
        echo "Usage: $0 [option]"
        echo
        echo "Options:"
        echo "  setup         Full setup (default)"
        echo "  backend-only  Setup backend only"
        echo "  frontend-only Setup frontend only"
        echo "  help          Show this help message"
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac