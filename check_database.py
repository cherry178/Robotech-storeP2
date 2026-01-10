#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password_here',  # Update this with your actual password
    'database': 'robotech_store'
}

def check_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Check total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        print(f"📊 Total products in database: {total}")

        # Check for Arduino Lilypad specifically
        cursor.execute("SELECT id, name FROM products WHERE name LIKE '%Lilypad%'")
        lilypad = cursor.fetchall()
        if lilypad:
            print("❌ FOUND Arduino Lilypad:")
            for prod_id, name in lilypad:
                print(f"   - ID {prod_id}: {name}")
        else:
            print("✅ No Arduino Lilypad found")

        # Show first 10 products
        cursor.execute("SELECT id, name FROM products ORDER BY id LIMIT 10")
        products = cursor.fetchall()
        print("\n📋 First 10 products in database:")
        for prod_id, name in products:
            print(f"   - ID {prod_id}: {name}")

        # Check if IDs 1, 2, 36, 41 exist with correct names
        cursor.execute("SELECT id, name FROM products WHERE id IN (1, 2, 36, 41)")
        key_products = cursor.fetchall()
        print("\n🔑 Key products (should match frontend expectations):")
        for prod_id, name in key_products:
            print(f"   - ID {prod_id}: {name}")

    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    check_database()
