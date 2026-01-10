#!/usr/bin/env python3
"""
Test script to verify database clearing is working
Run this BEFORE restarting the backend to see current state
Run this AFTER restarting backend to verify clearing worked
"""

import mysql.connector
from mysql.connector import Error

# Update this with your actual MySQL password
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',  # CHANGE THIS!
    'database': 'robotech_store'
}

def test_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("🔍 TESTING DATABASE STATE...")

        # Check total products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        print(f"📊 Total products: {total_products}")

        # Check total cart items
        cursor.execute("SELECT COUNT(*) FROM cart")
        total_cart = cursor.fetchone()[0]
        print(f"🛒 Total cart items: {total_cart}")

        # Check for Arduino Lilypad
        cursor.execute("SELECT id, name FROM products WHERE name LIKE '%Lilypad%'")
        lilypad = cursor.fetchall()
        if lilypad:
            print("❌ FOUND Arduino Lilypad:")
            for prod_id, name in lilypad:
                print(f"   - ID {prod_id}: {name}")
        else:
            print("✅ No Arduino Lilypad found")

        # Check for PCB Antenna
        cursor.execute("SELECT id, name FROM products WHERE name LIKE '%PCB Antenna%'")
        antenna = cursor.fetchall()
        if antenna:
            print("❌ FOUND PCB Antenna:")
            for prod_id, name in antenna:
                print(f"   - ID {prod_id}: {name}")
        else:
            print("✅ No PCB Antenna found")

        # Check your expected products
        expected_products = [
            (1, "Arduino Uno R3"),
            (2, "ESP32 Development Board"),
            (36, "Raspberry Pi Zero W"),
            (41, "Adafruit Feather M0")
        ]

        print("\n🎯 CHECKING YOUR EXPECTED PRODUCTS:")
        all_correct = True
        for exp_id, exp_name in expected_products:
            cursor.execute("SELECT name FROM products WHERE id = %s", (exp_id,))
            result = cursor.fetchone()
            if result and result[0] == exp_name:
                print(f"   - ID {exp_id}: {result[0]} ✅")
            else:
                actual = result[0] if result else "NOT FOUND"
                print(f"   - ID {exp_id}: {actual} ❌ (expected: {exp_name})")
                all_correct = False

        if all_correct and total_products == 62:
            print("\n🎉 DATABASE LOOKS CORRECT!")
        else:
            print(f"\n⚠️ DATABASE ISSUES: Expected 62 products, found {total_products}")

    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    test_database()
