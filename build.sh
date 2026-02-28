#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium

echo "Creating required directories..."
mkdir -p data/logs data/resumes data/job_listings uploads

echo "Build complete!"
