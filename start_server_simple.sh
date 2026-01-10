#!/bin/bash

# Simple Server Startup Script for Robotech Store
# This script starts the Flask server on port 8888

echo "🚀 Starting Robotech Store Server..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if backend/app.py exists
if [ ! -f "backend/app.py" ]; then
    echo "❌ backend/app.py not found!"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt --quiet
fi

# Kill any existing process on port 8888
if lsof -ti:8888 >/dev/null 2>&1; then
    echo "🛑 Stopping existing server on port 8888..."
    lsof -ti:8888 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Start the server
echo "🚀 Starting Flask server on port 8888..."
echo "🌐 Server will be available at: http://127.0.0.1:8888"
echo "📱 For mobile: Use your computer's IP address (e.g., http://192.168.1.100:8888)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

cd backend
python3 app.py
