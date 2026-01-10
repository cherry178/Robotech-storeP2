#!/bin/bash

# Check if Robotech Store Server is running

echo "🔍 Checking Robotech Store Server Status..."
echo ""

# Check if port 8888 is in use
if lsof -ti:8888 >/dev/null 2>&1; then
    PID=$(lsof -ti:8888)
    echo "✅ Server is RUNNING"
    echo "   Process ID (PID): $PID"
    echo "   Port: 8888"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Local: http://127.0.0.1:8888"
    echo "   Network: http://0.0.0.0:8888"
    echo ""
    
    # Get IP address for mobile access
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
    if [ ! -z "$IP" ]; then
        echo "📱 Mobile Access:"
        echo "   http://$IP:8888"
    fi
    echo ""
    echo "📋 Recent logs:"
    if [ -f "logs/server.log" ]; then
        tail -5 logs/server.log
    fi
else
    echo "❌ Server is NOT running"
    echo ""
    echo "🚀 To start the server, run:"
    echo "   ./start_background_server.sh"
fi
