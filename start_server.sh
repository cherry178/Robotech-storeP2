#!/bin/bash

# Robotech Store - Enhanced Startup Script
echo "🚀 Starting Robotech Store..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if the comprehensive startup script exists
if [ -f "start_project.sh" ]; then
    echo "Using comprehensive startup script..."
    exec ./start_project.sh
else
    echo "⚠️  Comprehensive startup script not found."
    echo "Starting basic HTTP server on port 8080..."
    echo ""
    python3 -m http.server 8080
    echo ""
    echo "Server stopped. Press Enter to exit."
    read
fi
