#!/bin/bash

# Stop Robotech Store Server

echo "🛑 Stopping Robotech Store Server..."

# Find and kill process on port 8888
if lsof -ti:8888 >/dev/null 2>&1; then
    PID=$(lsof -ti:8888)
    echo "   Found server process (PID: $PID)"
    kill $PID 2>/dev/null
    sleep 2
    
    # Force kill if still running
    if lsof -ti:8888 >/dev/null 2>&1; then
        echo "   Force stopping..."
        kill -9 $PID 2>/dev/null
    fi
    
    echo "✅ Server stopped successfully"
else
    echo "ℹ️  No server running on port 8888"
fi

# Also try to kill by process name
pkill -f "python.*app.py" 2>/dev/null

echo "✅ Done!"
