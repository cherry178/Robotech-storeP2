#!/usr/bin/env python3
"""
Script to show what products are currently displayed in the frontend
by fetching from the backend API just like the frontend does.
"""

import requests
import json
import time

def show_frontend_products():
    """Fetch and display products as they appear in the frontend"""

    # Wait a moment for servers to start
    time.sleep(2)

    print("🔍 Checking if backend is running...")
    print("📡 Fetching products from: http://127.0.0.1:8888/api/products?page=1&limit=12")
    print()

    try:
        # Fetch products from backend API (same as frontend)
        response = requests.get('http://127.0.0.1:8888/api/products?page=1&limit=12', timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get('success'):
                products = data.get('products', [])
                total = data.get('total', 0)

                print(f"✅ BACKEND RESPONSE SUCCESSFUL")
                print(f"📦 Total products in database: {total}")
                print(f"📄 Products on current page: {len(products)}")
                print("=" * 80)
                print("🎯 PRODUCTS CURRENTLY DISPLAYED IN FRONTEND:")
                print("=" * 80)

                for i, product in enumerate(products, 1):
                    print(f"#{i} 🆔 ID: {product['id']}")
                    print(f"   📝 Name: {product['name']}")
                    print(f"   💰 Price: ₹{product['price']}")
                    print(f"   📂 Category: {product['category']}")
                    print(f"   📦 Stock: {product.get('stock_quantity', 'N/A')}")
                    print(f"   ⭐ Featured: {'Yes' if product.get('is_featured') else 'No'}")
                    print(f"   🖼️  Image URL: {product.get('image_url', 'N/A')}")
                    print(f"   📋 Description: {product.get('description', 'N/A')[:60]}...")
                    print("-" * 60)

                print(f"\n📊 SUMMARY:")
                print(f"   • Products loaded: {len(products)}")
                print(f"   • Total available: {total}")
                print(f"   • Page: 1 of {max(1, (total + 11) // 12)}")

                # Group by categories
                categories = {}
                for product in products:
                    cat = product['category']
                    categories[cat] = categories.get(cat, 0) + 1

                print(f"   • Categories shown: {', '.join(f'{cat} ({count})' for cat, count in categories.items())}")

            else:
                print("❌ Backend returned error:")
                print(f"   Error: {data.get('error', 'Unknown error')}")

        else:
            print(f"❌ Backend returned HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}...")

    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Backend server is not running!")
        print("   Please start the backend with: python backend/app.py")

    except requests.exceptions.Timeout:
        print("❌ TIMEOUT ERROR: Backend server took too long to respond")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print("\n💡 FRONTEND BEHAVIOR:")
    print("   • Frontend fetches 12 products per page")
    print("   • Uses pagination for navigation")
    print("   • Displays products in a grid layout")
    print("   • Shows product images, names, prices, and 'Add to Cart' buttons")
    print("   • Filters work by category and search terms")

if __name__ == '__main__':
    show_frontend_products()
