#!/usr/bin/env python3
"""
Test that API returns correct products for each category
"""

import sys
sys.path.insert(0, 'backend')
from app import DEMO_PRODUCTS

def test_category_filtering():
    print("🧪 TESTING CATEGORY FILTERING...")

    # Test each category
    categories_to_test = [
        ('Microcontrollers', 11),
        ('Actuators', 9),
        ('Sensors', 15),
        ('Displays', 7),
        ('Power Supply', 6),
        ('Tools & Accessories', 6),
        ('Audio Components', 6)
    ]

    all_passed = True

    for category_name, expected_count in categories_to_test:
        # Simulate API filtering
        filtered_products = [p for p in DEMO_PRODUCTS if p['category'].lower() == category_name.lower()]

        if len(filtered_products) == expected_count:
            print(f"✅ {category_name}: {len(filtered_products)} products")
        else:
            print(f"❌ {category_name}: {len(filtered_products)} products (expected {expected_count})")
            all_passed = False

            # Show what we got
            for p in filtered_products[:3]:
                print(f"   - {p['name']}")
            if len(filtered_products) > 3:
                print(f"   ... and {len(filtered_products) - 3} more")

    # Test "all" category
    all_products = len(DEMO_PRODUCTS)
    if all_products == 60:
        print(f"✅ All products: {all_products} products")
    else:
        print(f"❌ All products: {all_products} products (expected 60)")
        all_passed = False

    if all_passed:
        print("\n🎉 ALL CATEGORY TESTS PASSED!")
    else:
        print("\n❌ SOME CATEGORY TESTS FAILED!")

    return all_passed

if __name__ == "__main__":
    test_category_filtering()
