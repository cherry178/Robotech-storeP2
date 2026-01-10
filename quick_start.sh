#!/bin/bash

# Quick Start Script for Robotech Store
# Run this to start the entire project with one command

echo "🚀 Quick Starting Robotech Store..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if main script exists
if [ -f "start_project.sh" ]; then
    # Run the main startup script
    exec ./start_project.sh
else
    echo "❌ Main startup script not found. Please run setup first."
    exit 1
fi
