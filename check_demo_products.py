#!/usr/bin/env python3
"""
Check if DEMO_PRODUCTS is properly loaded in the backend
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

try:
    from app import DEMO_PRODUCTS
    print(f"✅ Successfully imported DEMO_PRODUCTS")
    print(f"📊 Total products in DEMO_PRODUCTS: {len(DEMO_PRODUCTS)}")

    if len(DEMO_PRODUCTS) > 0:
        print("📋 First 3 products:")
        for i, product in enumerate(DEMO_PRODUCTS[:3]):
            print(f"   - ID {product['id']}: {product['name']} (₹{product['price']})")

        print("📋 Last 3 products:")
        for i, product in enumerate(DEMO_PRODUCTS[-3:]):
            print(f"   - ID {product['id']}: {product['name']} (₹{product['price']})")

        # Check for your expected products
        expected_ids = [1, 2, 36, 41]
        print("\n🎯 Checking expected products:")
        for expected_id in expected_ids:
            product = next((p for p in DEMO_PRODUCTS if p['id'] == expected_id), None)
            if product:
                print(f"   - ID {expected_id}: {product['name']} ✅")
            else:
                print(f"   - ID {expected_id}: NOT FOUND ❌")

        # Check for bad products
        bad_products = [p for p in DEMO_PRODUCTS if 'Lilypad' in p['name'] or 'PCB Antenna' in p['name']]
        if bad_products:
            print("\n❌ Found unwanted products in DEMO_PRODUCTS:")
            for product in bad_products:
                print(f"   - ID {product['id']}: {product['name']}")
        else:
            print("\n✅ No unwanted products found in DEMO_PRODUCTS")
    else:
        print("❌ DEMO_PRODUCTS is empty!")

except ImportError as e:
    print(f"❌ Failed to import DEMO_PRODUCTS: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
