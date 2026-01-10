#!/bin/bash

# Start Robotech Store Server in Background
# This will keep running even after closing Terminal/Cursor

echo "🚀 Starting Robotech Store Server in Background..."
echo ""

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

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Start the server in background using nohup
echo "🚀 Starting Flask server in background on port 8888..."
cd backend

# Use nohup to run in background and redirect output
nohup python3 app.py > "$SCRIPT_DIR/logs/server.log" 2> "$SCRIPT_DIR/logs/server_error.log" &

# Get the process ID
SERVER_PID=$!

# Wait a moment to check if it started
sleep 3

# Check if server is running
if ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✅ Server started successfully!"
    echo ""
    echo "📋 Server Information:"
    echo "   Process ID (PID): $SERVER_PID"
    echo "   Status: Running in background"
    echo "   Logs: $SCRIPT_DIR/logs/server.log"
    echo "   Errors: $SCRIPT_DIR/logs/server_error.log"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Local: http://127.0.0.1:8888"
    echo "   Network: http://0.0.0.0:8888"
    echo ""
    echo "📱 For Mobile Access:"
    echo "   1. Make sure your phone and computer are on the same Wi-Fi"
    echo "   2. Find your computer's IP: ifconfig | grep 'inet ' | grep -v 127.0.0.1"
    echo "   3. Open on phone: http://YOUR_IP:8888"
    echo ""
    echo "🛑 To stop the server, run:"
    echo "   ./stop_server.sh"
    echo "   OR"
    echo "   kill $SERVER_PID"
    echo ""
    echo "✅ Server will continue running even after closing Terminal/Cursor!"
else
    echo "❌ Failed to start server. Check logs for errors:"
    echo "   tail -f $SCRIPT_DIR/logs/server_error.log"
    exit 1
fi
