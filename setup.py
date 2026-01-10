#!/usr/bin/env python3
"""
Setup script for Robotech Store
Initializes the MySQL database and installs required dependencies
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def setup_database():
    """Setup MySQL database and tables"""
    print("🔧 Setting up MySQL database...")

    try:
        # Connect to MySQL (assuming root user with no password for development)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS robotech_store")
            print("✅ Database 'robotech_store' created successfully")

            # Use the database
            cursor.execute("USE robotech_store")

            # Read and execute schema
            with open('database_schema.sql', 'r') as file:
                schema_sql = file.read()

            # Split SQL commands and execute them
            commands = schema_sql.split(';')
            for command in commands:
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                    except Error as e:
                        if "database_schema" not in str(e):  # Ignore USE database error
                            print(f"Warning: {e}")

            print("✅ Database schema created successfully")

            # Load sample data
            with open('sample_data.sql', 'r') as file:
                sample_sql = file.read()

            commands = sample_sql.split(';')
            for command in commands:
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                    except Error as e:
                        print(f"Warning loading sample data: {e}")

            print("✅ Sample data loaded successfully")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"❌ Database setup failed: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def create_env_file():
    """Create environment configuration file"""
    env_content = """# Robotech Store Environment Configuration

# Flask Configuration
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=robotech_store

# Email Configuration (for future use)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Payment Configuration (for future use)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
"""

    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Environment file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create environment file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Robotech Store...")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists('backend/app.py'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)

    success = True

    # Install Python dependencies
    if not install_dependencies():
        success = False

    # Create environment file
    if not create_env_file():
        success = False

    # Setup database
    if not setup_database():
        success = False

    print("=" * 50)

    if success:
        print("🎉 Robotech Store setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure MySQL server is running")
        print("2. Run: python backend/app.py")
        print("3. Open http://localhost:5000 in your browser")
        print("\nFor phone authentication, check the browser console for demo OTPs")
    else:
        print("❌ Setup completed with errors. Please check the messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
