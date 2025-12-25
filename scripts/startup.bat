@echo off
REM ==========================================
REM AutoAgentHire Startup Script for Windows
REM ==========================================

echo ========================================
echo    AutoAgentHire - AI Job Automation
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "logs\" mkdir logs
if not exist "uploads\resumes\" mkdir uploads\resumes
if not exist "uploads\cover_letters\" mkdir uploads\cover_letters

REM Start backend in background
echo Starting backend...
start /B uvicorn backend.main:app --reload --port 8000 > logs\backend.log 2>&1

REM Wait for backend
timeout /t 5 /nobreak > nul

REM Start frontend
echo Starting frontend...
streamlit run frontend\streamlit\app_enhanced.py --server.port 8501

echo.
echo ========================================
echo  AutoAgentHire is running!
echo ========================================
echo  Frontend: http://localhost:8501
echo  Backend:  http://localhost:8000
echo ========================================
