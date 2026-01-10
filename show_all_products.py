#!/usr/bin/env python3

import re

def extract_products_from_file():
    """Extract all products from the backend app.py file"""
    with open('backend/app.py', 'r') as f:
        content = f.read()

    # Find the DEMO_PRODUCTS list
    start = content.find('DEMO_PRODUCTS = [')
    if start == -1:
        return []

    # Find the end of the list (closing bracket)
    bracket_count = 0
    end = start
    for i, char in enumerate(content[start:], start):
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end = i + 1
                break

    products_text = content[start:end]

    # Use regex to extract individual product dictionaries
    products = []
    product_pattern = r'{\s*"id":\s*(\d+),\s*"name":\s*"([^"]+)",\s*"description":\s*"([^"]*)",\s*"price":\s*([\d.]+),\s*"category":\s*"([^"]+)",\s*"stock_quantity":\s*(\d+),\s*"image_url":\s*"([^"]+)",\s*"is_featured":\s*(true|false)\s*}'

    for match in re.finditer(product_pattern, products_text, re.MULTILINE | re.DOTALL):
        product = {
            'id': int(match.group(1)),
            'name': match.group(2),
            'description': match.group(3),
            'price': float(match.group(4)),
            'category': match.group(5),
            'stock_quantity': int(match.group(6)),
            'image_url': match.group(7),
            'is_featured': match.group(8) == 'true'
        }
        products.append(product)

    return products

def show_products_summary(products):
    """Show a summary of all products"""
    print(f'📦 ALL PRODUCTS IN DATABASE ({len(products)} total):\n')

    # Group by category
    categories = {}
    featured_count = 0

    for product in products:
        cat = product['category']
        categories[cat] = categories.get(cat, []) + [product]
        if product['is_featured']:
            featured_count += 1

    print(f'📊 SUMMARY:')
    print(f'   • Total Products: {len(products)}')
    print(f'   • Featured Products: {featured_count}')
    print(f'   • Categories: {len(categories)}')
    print()

    # Show products by category
    for category, prods in sorted(categories.items()):
        print(f'📂 {category} ({len(prods)} products):')
        for product in sorted(prods, key=lambda x: x['id']):
            featured = "⭐" if product['is_featured'] else "  "
            print(f'   {featured} #{product["id"]:2d}: {product["name"]} - ₹{product["price"]}')
        print()

def show_all_products(products):
    """Show all products in detail"""
    print(f'📦 ALL PRODUCTS IN DATABASE ({len(products)} total):\n')

    for product in sorted(products, key=lambda x: x['id']):
        print(f'🆔 ID: {product["id"]}')
        print(f'📝 Name: {product["name"]}')
        print(f'💰 Price: ₹{product["price"]}')
        print(f'📂 Category: {product["category"]}')
        print(f'📦 Stock: {product["stock_quantity"]}')
        print(f'⭐ Featured: {"Yes" if product["is_featured"] else "No"}')
        print(f'📋 Description: {product["description"][:80]}...' if len(product["description"]) > 80 else f'📋 Description: {product["description"]}')
        print(f'🖼️  Image: {product["image_url"]}')
        print('-' * 60)

if __name__ == '__main__':
    products = extract_products_from_file()
    show_products_summary(products)
    print('=' * 80)
    print('Showing first 10 products in detail:')
    show_all_products(products[:10])
