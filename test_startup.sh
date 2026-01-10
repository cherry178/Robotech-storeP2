#!/bin/bash

# Test script to verify startup components
echo "🧪 Testing Robotech Store Startup Components..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Test 1: Check if scripts exist and are executable
echo "1. Checking startup scripts..."
if [ -x "start_project.sh" ]; then
    echo "   ✅ start_project.sh exists and is executable"
else
    echo "   ❌ start_project.sh missing or not executable"
fi

if [ -x "quick_start.sh" ]; then
    echo "   ✅ quick_start.sh exists and is executable"
else
    echo "   ❌ quick_start.sh missing or not executable"
fi

# Test 2: Check macOS app
if [ -d "RobotechStore.app" ] && [ -x "RobotechStore.app/Contents/MacOS/RobotechStore" ]; then
    echo "   ✅ RobotechStore.app exists and is executable"
else
    echo "   ❌ RobotechStore.app missing or not executable"
fi

# Test 3: Check backend files
echo ""
echo "2. Checking backend components..."
if [ -f "backend/app.py" ]; then
    echo "   ✅ backend/app.py exists"
else
    echo "   ❌ backend/app.py missing"
fi

if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt exists"
else
    echo "   ❌ requirements.txt missing"
fi

# Test 4: Check frontend files
echo ""
echo "3. Checking frontend components..."
if [ -d "templates" ] && [ -f "templates/index.html" ]; then
    echo "   ✅ Frontend templates exist"
else
    echo "   ❌ Frontend templates missing"
fi

if [ -d "static" ]; then
    echo "   ✅ Static files directory exists"
else
    echo "   ❌ Static files directory missing"
fi

# Test 5: Check README
echo ""
echo "4. Checking documentation..."
if [ -f "README_STARTUP.md" ]; then
    echo "   ✅ README_STARTUP.md exists"
else
    echo "   ❌ README_STARTUP.md missing"
fi

echo ""
echo "🎉 Startup component check complete!"
echo ""
echo "To start the project, use one of these methods:"
echo "• macOS: Double-click RobotechStore.app"
echo "• Terminal: ./quick_start.sh"
echo "• Advanced: ./start_project.sh"
