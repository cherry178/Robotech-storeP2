#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

# Update this with your actual MySQL password
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password_here',
    'database': 'robotech_store'
}

def verify_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("🔍 VERIFYING DATABASE CONTENTS...")

        # Check total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        print(f"📊 Total products in database: {total}")

        # Check for Arduino Lilypad specifically
        cursor.execute("SELECT id, name FROM products WHERE name LIKE '%Lilypad%' OR id = 26")
        lilypad = cursor.fetchall()
        if lilypad:
            print("❌ FOUND Arduino Lilypad (ID 26):")
            for prod_id, name in lilypad:
                print(f"   - ID {prod_id}: {name}")
        else:
            print("✅ No Arduino Lilypad found")

        # Check what product ID 26 actually is
        cursor.execute("SELECT id, name FROM products WHERE id = 26")
        product_26 = cursor.fetchall()
        if product_26:
            print("🔍 Product ID 26:")
            for prod_id, name in product_26:
                print(f"   - ID {prod_id}: {name}")
        else:
            print("✅ No product with ID 26")

        # Show your expected products
        print("\n🎯 YOUR EXPECTED PRODUCTS (from DEMO_PRODUCTS):")
        expected_ids = [1, 2, 36, 41]
        for expected_id in expected_ids:
            cursor.execute("SELECT id, name FROM products WHERE id = %s", (expected_id,))
            result = cursor.fetchall()
            if result:
                prod_id, name = result[0]
                print(f"   - ID {prod_id}: {name} ✅")
            else:
                print(f"   - ID {expected_id}: MISSING ❌")

    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    verify_database()
