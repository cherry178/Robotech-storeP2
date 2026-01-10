#!/usr/bin/env python3
"""
Run script for Robotech Store
Starts the Flask development server
"""

import os
import sys
import subprocess

def check_mysql_connection():
    """Check if MySQL server is running and accessible"""
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            connection_timeout=5
        )
        connection.close()
        return True
    except:
        return False

def start_mysql_service():
    """Try to start MySQL service (macOS)"""
    try:
        print("🔧 Attempting to start MySQL service...")
        result = subprocess.run(['brew', 'services', 'start', 'mysql'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL service started successfully")
            import time
            time.sleep(3)  # Wait for MySQL to fully start
            return True
        else:
            print("❌ Failed to start MySQL service")
            return False
    except:
        return False

def main():
    """Main run function"""
    print("🚀 Starting Robotech Store...")
    print("=" * 50)

    # Check if MySQL is running
    if not check_mysql_connection():
        print("⚠️  MySQL server is not running or not accessible.")
        print("   Please ensure MySQL is installed and running.")
        print("   On macOS: brew install mysql && brew services start mysql")
        print("   On Ubuntu: sudo systemctl start mysql")
        print("   On Windows: Start MySQL from Services panel")
        print()

        print("⚠️  MySQL not available. Running in demo mode...")
        print("   Note: Some features may be limited without database.")
        print()

    # Check if required files exist
    required_files = [
        'backend/app.py',
        'requirements.txt'
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file '{file}' not found.")
            sys.exit(1)

    # Check if virtual environment exists
    venv_path = 'venv'
    if os.path.exists(venv_path):
        print("✅ Virtual environment found")
        python_cmd = os.path.join(venv_path, 'bin', 'python')
        pip_cmd = os.path.join(venv_path, 'bin', 'pip')
    else:
        print("ℹ️  Using system Python")
        python_cmd = 'python'
        pip_cmd = 'pip'

    # Install/update dependencies
    print("🔧 Installing/updating dependencies...")
    try:
        subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'],
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

    # Start the Flask application
    print("🚀 Starting Flask development server...")
    print("   Server will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)

    try:
        os.chdir('backend')
        subprocess.run([python_cmd, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError:
        print("❌ Failed to start Flask server")
        sys.exit(1)

if __name__ == "__main__":
    main()
