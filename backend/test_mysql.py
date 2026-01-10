#!/usr/bin/env python3
"""
Test MySQL connection and database setup
Run this to verify MySQL is working correctly
"""

import mysql.connector
from mysql.connector import Error

# Same config as main app
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',  # Update this with your MySQL password
    'database': 'robotech_store'
}

def test_connection():
    """Test basic MySQL connection"""
    print("🔍 Testing MySQL connection...")

    # Test without database first
    base_config = {
        'host': DB_CONFIG['host'],
        'user': DB_CONFIG['user'],
        'password': DB_CONFIG['password']
    }

    try:
        connection = mysql.connector.connect(**base_config)
        print("✅ Basic MySQL connection successful")
        connection.close()
    except Error as e:
        print(f"❌ Basic MySQL connection failed: {e}")
        print("💡 Check if MySQL server is running and credentials are correct")
        return False

    # Test with database
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("✅ Database connection successful")
        cursor = connection.cursor()

        # Test tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        print(f"📋 Found tables: {table_names}")

        required_tables = ['users', 'products', 'cart']
        missing_tables = [table for table in required_tables if table not in table_names]

        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            print("💡 Run: python backend/setup_mysql.py")
            return False
        else:
            print("✅ All required tables exist")

        # Test cart operations
        print("\n🧪 Testing cart operations...")

        # Check if we can insert a test item
        test_user_id = 999
        test_product_id = 1

        # First, create a test user (to satisfy foreign key constraint)
        cursor.execute("""
            INSERT INTO users (id, phone, name)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE phone = VALUES(phone)
        """, (test_user_id, '9999999999', 'Test User'))

        # Clean up any existing test cart data
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (test_user_id,))

        # Try to insert cart item
        cursor.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (test_user_id, test_product_id, 1))

        connection.commit()
        print("✅ Test cart insert successful")

        # Try to read it back
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.name, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (test_user_id,))

        result = cursor.fetchone()
        if result:
            print(f"✅ Test cart read successful: {result}")
        else:
            print("❌ Test cart read failed")

        # Clean up test data
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (test_user_id,))
        cursor.execute("DELETE FROM users WHERE id = %s", (test_user_id,))
        connection.commit()
        print("🧹 Test data cleaned up")

        cursor.close()
        connection.close()

        print("\n🎉 MySQL setup is working correctly!")
        return True

    except Error as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing MySQL setup for Robotech Store...\n")

    # Check password
    if not DB_CONFIG['password']:
        print("⚠️  MySQL password is empty in DB_CONFIG")
        print("   This will likely fail - update the password in:")
        print("   - backend/test_mysql.py")
        print("   - backend/app.py")
        print("   Example: 'password': 'your_mysql_password'")
        print()

    success = test_connection()

    if success:
        print("\n✅ All MySQL tests passed!")
        print("💡 Your cart API should work now")
        print("   Try adding items to cart in the frontend")
    else:
        print("\n❌ MySQL tests failed!")
        print("💡 Check the error messages above and fix issues")

if __name__ == "__main__":
    main()
