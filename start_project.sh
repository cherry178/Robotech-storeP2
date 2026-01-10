#!/bin/bash

# Robotech Store - Complete Project Startup Script
# This script starts all necessary services for the Robotech Store project

echo "🚀 Starting Robotech Store Project..."
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to check if a process is running on a port
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        print_warning "Killing process $pid on port $port"
        kill $pid 2>/dev/null
        sleep 2
        if kill -0 $pid 2>/dev/null; then
            kill -9 $pid 2>/dev/null
        fi
    fi
}

# Function to check MySQL connection
check_mysql() {
    print_status "Checking MySQL connection..."
    if mysql -u root -e "SELECT 1;" >/dev/null 2>&1; then
        print_success "MySQL is running and accessible"
        return 0
    else
        print_warning "MySQL is not accessible"
        return 1
    fi
}

# Function to start MySQL (macOS with brew)
start_mysql() {
    print_status "Attempting to start MySQL service..."

    # Try brew services first (macOS)
    if command -v brew >/dev/null 2>&1; then
        if brew services start mysql 2>/dev/null; then
            print_success "MySQL service started via brew"
            sleep 3
            return 0
        fi
    fi

    # Try systemctl (Linux)
    if command -v systemctl >/dev/null 2>&1; then
        if sudo systemctl start mysql 2>/dev/null || sudo systemctl start mysqld 2>/dev/null; then
            print_success "MySQL service started via systemctl"
            sleep 3
            return 0
        fi
    fi

    # Try service command (older Linux)
    if command -v service >/dev/null 2>&1; then
        if sudo service mysql start 2>/dev/null || sudo service mysqld start 2>/dev/null; then
            print_success "MySQL service started via service command"
            sleep 3
            return 0
        fi
    fi

    print_error "Could not start MySQL service automatically"
    print_warning "Please start MySQL manually:"
    echo "  macOS: brew services start mysql"
    echo "  Ubuntu/Debian: sudo systemctl start mysql"
    echo "  CentOS/RHEL: sudo systemctl start mysqld"
    echo "  Windows: Start MySQL from Services panel"
    return 1
}

# Function to start Flask backend
start_backend() {
    print_status "Starting Flask backend server..."

    # Kill any existing process on port 8888
    kill_port 8888

    # Navigate to backend directory
    cd "$SCRIPT_DIR/backend"

    # Check if virtual environment exists
    if [ -d "venv" ]; then
        print_status "Using virtual environment"
        source venv/bin/activate
        PYTHON_CMD="venv/bin/python"
    else
        print_status "Using system Python"
        PYTHON_CMD="python3"
    fi

    # Install/update dependencies
    print_status "Installing/updating dependencies..."
    if pip install -r "$SCRIPT_DIR/requirements.txt" >/dev/null 2>&1; then
        print_success "Dependencies installed"
    else
        print_warning "Could not install dependencies (continuing anyway)"
    fi

    # Start Flask server in background
    print_status "Starting Flask server on port 8888..."
    nohup $PYTHON_CMD app.py > "$SCRIPT_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!

    # Wait a bit and check if it's running
    sleep 3
    if check_port 8888; then
        print_success "Flask backend started successfully (PID: $BACKEND_PID)"
        print_status "Backend URL: http://localhost:8888"
        return 0
    else
        print_error "Failed to start Flask backend"
        return 1
    fi
}

# Function to start frontend (if needed)
start_frontend() {
    # Check if there's a separate frontend to start
    if [ -f "package.json" ]; then
        print_status "Frontend package.json found - starting frontend server..."

        # Kill any existing process on port 3000 (common React port)
        kill_port 3000

        # Start frontend server
        if command -v npm >/dev/null 2>&1; then
            nohup npm start > "$SCRIPT_DIR/frontend.log" 2>&1 &
            FRONTEND_PID=$!
            sleep 5
            if check_port 3000; then
                print_success "Frontend server started on port 3000 (PID: $FRONTEND_PID)"
                return 0
            fi
        fi
    fi

    # Check if we need to start a simple HTTP server for static files
    if [ -f "index.html" ] && [ ! -f "package.json" ]; then
        print_status "Starting simple HTTP server for frontend..."

        # Kill any existing process on port 7000
        kill_port 7000

        cd "$SCRIPT_DIR"
        nohup python3 -m http.server 7000 > "$SCRIPT_DIR/frontend.log" 2>&1 &
        FRONTEND_PID=$!
        sleep 2
        if check_port 7000; then
            print_success "Frontend HTTP server started on port 7000 (PID: $FRONTEND_PID)"
            return 0
        fi
    fi

    print_status "No frontend server needed or could not start frontend"
    return 0
}

# Function to show status
show_status() {
    echo ""
    echo "========================================"
    print_success "Robotech Store is now running!"
    echo ""
    echo "🌐 Available URLs:"
    echo "   Backend API:  http://localhost:8888"
    if check_port 7000; then
        echo "   Frontend:      http://localhost:7000"
    fi
    if check_port 3000; then
        echo "   Frontend:      http://localhost:3000"
    fi
    echo ""
    echo "📝 Test the following:"
    echo "   Home:          http://localhost:8888/"
    echo "   Products:      http://localhost:8888/products"
    echo "   Cart:          http://localhost:8888/cart"
    echo "   Orders:        http://localhost:8888/orders"
    echo ""
    print_warning "Press Ctrl+C to stop all services"
    echo "========================================"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    print_status "Shutting down services..."

    # Kill backend
    if [ ! -z "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
        print_status "Stopping Flask backend (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
    fi

    # Kill frontend
    if [ ! -z "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
        print_status "Stopping frontend server (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
    fi

    print_success "All services stopped"
    exit 0
}

# Set trap for cleanup on exit
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    local mysql_ok=0
    local backend_ok=0
    local frontend_ok=0

    # Check MySQL
    if check_mysql; then
        mysql_ok=1
    else
        if start_mysql; then
            mysql_ok=1
        fi
    fi

    # Start backend
    if start_backend; then
        backend_ok=1
    fi

    # Start frontend
    if start_frontend; then
        frontend_ok=1
    fi

    # Show status
    if [ $backend_ok -eq 1 ]; then
        show_status

        # Keep script running
        print_status "Services are running. Press Ctrl+C to stop."
        while true; do
            sleep 1
        done
    else
        print_error "Failed to start essential services. Check logs for details."
        exit 1
    fi
}

# Run main function
main
