#!/usr/bin/env python3
"""
Test MySQL connection to verify database access
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',
    'database': 'robotech_store'
}

def test_connection():
    print("🔍 TESTING MYSQL CONNECTION...")
    try:
        print(f"Connecting to: {DB_CONFIG['host']} as {DB_CONFIG['user']}")
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✅ MySQL connection successful!")

        cursor = connection.cursor()

        # Test basic queries
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Basic query works: {result}")

        # Check if robotech_store database exists
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()
        print(f"✅ Current database: {current_db[0]}")

        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"📋 Tables in database: {[table[0] for table in tables]}")

        # Check products table
        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]
        print(f"📊 Products in database: {count}")

        cursor.close()
        connection.close()
        print("✅ Connection test completed successfully!")

    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

    return True

if __name__ == "__main__":
    test_connection()
