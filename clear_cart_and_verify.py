#!/usr/bin/env python3
"""
Clear all cart items and verify product IDs match DEMO_PRODUCTS
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app import get_db_connection, DEMO_PRODUCTS, Error

def clear_cart_and_verify():
    print("🧹 CLEARING CART AND VERIFYING PRODUCT IDs...")
    
    connection = get_db_connection()
    if not connection:
        print("❌ Could not connect to MySQL database")
        return
    
    try:
        cursor = connection.cursor()
        
        # Clear all cart items
        cursor.execute("DELETE FROM cart")
        deleted = cursor.rowcount
        connection.commit()
        print(f"🗑️ Cleared {deleted} items from cart")
        
        # Verify product IDs
        print("\n🔍 VERIFYING PRODUCT IDs IN DATABASE...")
        
        # Check specific products
        important_products = [
            {"id": 34, "expected_name": "Touch Sensor"},
            {"id": 52, "expected_name": "Nuts & Bolts Kit"},
            {"id": 29, "expected_name": "Breadboard"},
            {"id": 30, "expected_name": "Male-Male Jumper Wires"},
            {"id": 31, "expected_name": "Male-Female Jumper Wires"}
        ]
        
        all_correct = True
        for check in important_products:
            product_id = check["id"]
            expected_name = check["expected_name"]
            
            cursor.execute("SELECT id, name FROM products WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            
            if result:
                db_id, db_name = result
                if db_name == expected_name:
                    print(f"✅ ID {product_id}: {db_name} (CORRECT)")
                else:
                    print(f"❌ ID {product_id}: Database has '{db_name}' but expected '{expected_name}'")
                    all_correct = False
            else:
                print(f"❌ ID {product_id}: NOT FOUND in database")
                all_correct = False
        
        # Get total product count
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        print(f"\n📊 Total products in database: {total}")
        print(f"📊 Expected products from DEMO_PRODUCTS: {len(DEMO_PRODUCTS)}")
        
        if total != len(DEMO_PRODUCTS):
            print(f"⚠️ WARNING: Product count mismatch!")
            all_correct = False
        
        if all_correct:
            print("\n✅ All product IDs are correct!")
        else:
            print("\n⚠️ Some product IDs are incorrect. You may need to run init_database()")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    clear_cart_and_verify()
