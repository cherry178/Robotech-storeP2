#!/usr/bin/env python3
"""
Complete MySQL Setup for Robotech Store
This script will help you set up MySQL from scratch
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"📝 Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout.strip():
                print(f"📄 Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ Failed!")
            if result.stderr.strip():
                print(f"🚨 Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def setup_mysql():
    """Complete MySQL setup process"""
    print("🚀 Complete MySQL Setup for Robotech Store")
    print("=" * 50)

    # Step 1: Check if MySQL is installed
    print("\n📦 Step 1: Checking MySQL installation...")
    mysql_installed = run_command("mysql --version", "Checking MySQL version")

    if not mysql_installed:
        print("\n💡 MySQL not found. Installing MySQL...")

        # Detect OS and install MySQL
        if sys.platform.startswith('linux'):
            print("🐧 Detected Linux - installing MySQL...")
            run_command("sudo apt update", "Updating package list")
            run_command("sudo apt install -y mysql-server", "Installing MySQL Server")

        elif sys.platform == 'darwin':  # macOS
            print("🍎 Detected macOS - installing MySQL...")
            run_command("brew install mysql", "Installing MySQL via Homebrew")
            run_command("brew services start mysql", "Starting MySQL service")

        else:
            print("❌ Unsupported OS. Please install MySQL manually.")
            return False

    # Step 2: Start MySQL service
    print("\n🔄 Step 2: Starting MySQL service...")
    if sys.platform.startswith('linux'):
        run_command("sudo systemctl start mysql", "Starting MySQL service")
        run_command("sudo systemctl enable mysql", "Enabling MySQL to start on boot")
    elif sys.platform == 'darwin':
        run_command("brew services start mysql", "Starting MySQL service")

    # Wait a moment for MySQL to start
    print("⏳ Waiting for MySQL to start...")
    time.sleep(3)

    # Step 3: Secure MySQL installation
    print("\n🔐 Step 3: Setting up MySQL root password...")

    # Create a temporary SQL file to set up root password
    setup_sql = """
-- Set root password and create database
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'robotech123';
FLUSH PRIVILEGES;
CREATE DATABASE IF NOT EXISTS robotech_store;
GRANT ALL PRIVILEGES ON robotech_store.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
"""

    with open('/tmp/mysql_setup.sql', 'w') as f:
        f.write(setup_sql)

    # Run the setup
    success = run_command("sudo mysql < /tmp/mysql_setup.sql", "Setting up MySQL root user and database")

    if success:
        print("✅ MySQL root password set to: robotech123")
        print("✅ Database 'robotech_store' created")

        # Step 4: Update config files
        print("\n📝 Step 4: Updating configuration files...")

        # Update backend/app.py
        app_py_content = """# MySQL Database Configuration
# Update these credentials to match your MySQL setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'robotech123',  # MySQL root password
    'database': 'robotech_store'
}"""

        # Read current app.py
        with open('app.py', 'r') as f:
            content = f.read()

        # Replace DB_CONFIG
        import re
        updated_content = re.sub(
            r"DB_CONFIG = \{[^}]*\}",
            app_py_content.replace('\n', '\n'),
            content,
            flags=re.DOTALL
        )

        with open('app.py', 'w') as f:
            f.write(updated_content)

        print("✅ Updated backend/app.py with MySQL credentials")

        # Update test_mysql.py
        test_py_content = """DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'robotech123',  # MySQL root password
    'database': 'robotech_store'
}"""

        with open('test_mysql.py', 'r') as f:
            content = f.read()

        updated_content = re.sub(
            r"DB_CONFIG = \{[^}]*\}",
            test_py_content,
            content,
            flags=re.DOTALL
        )

        with open('test_mysql.py', 'w') as f:
            f.write(updated_content)

        print("✅ Updated test_mysql.py with MySQL credentials")

        # Step 5: Run database setup
        print("\n🗄️ Step 5: Creating database tables...")
        success = run_command("python setup_mysql.py", "Running database setup script")

        if success:
            # Step 6: Test the setup
            print("\n🧪 Step 6: Testing MySQL connection...")
            test_success = run_command("python test_mysql.py", "Running MySQL connection test")

            if test_success:
                print("\n" + "="*50)
                print("🎉 MySQL Setup Complete!")
                print("="*50)
                print("✅ MySQL server installed and running")
                print("✅ Root password set to: robotech123")
                print("✅ Database 'robotech_store' created")
                print("✅ Tables created and populated")
                print("✅ Connection test passed")
                print()
                print("🚀 Ready to run the Flask backend:")
                print("   cd ..")
                print("   python backend/app.py")
                print()
                print("🌐 Frontend will work at:")
                print("   http://127.0.0.1:7000/")
                print()
                print("💡 MySQL Credentials:")
                print("   Host: localhost")
                print("   User: root")
                print("   Password: robotech123")
                print("   Database: robotech_store")
                return True
            else:
                print("❌ MySQL test failed")
                return False
        else:
            print("❌ Database setup failed")
            return False
    else:
        print("❌ MySQL setup failed")
        return False

if __name__ == "__main__":
    # Check if running as root (needed for MySQL setup on Linux)
    if sys.platform.startswith('linux'):
        import os
        if os.geteuid() != 0:
            print("❌ This script needs to run as root on Linux (for MySQL setup)")
            print("💡 Run: sudo python backend/setup_mysql_complete.py")
            sys.exit(1)

    success = setup_mysql()
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
