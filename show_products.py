#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'robotech_store'
}

def show_products():
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Query all products
        cursor.execute('SELECT id, name, price, category, description, image_url FROM products ORDER BY id')
        products = cursor.fetchall()

        print(f'📦 Found {len(products)} products in the database:\n')

        for product in products:
            print(f'🆔 ID: {product["id"]}')
            print(f'📝 Name: {product["name"]}')
            print(f'💰 Price: ₹{product["price"]}')
            print(f'📂 Category: {product["category"]}')
            print(f'📋 Description: {product["description"][:100]}...' if product["description"] and len(product["description"]) > 100 else f'📋 Description: {product["description"]}')
            print(f'🖼️  Image: {product["image_url"]}')
            print('-' * 50)

    except Error as e:
        print(f'❌ Database error: {e}')

    finally:
        if 'connection' in locals() and connection and connection.is_connected():
            cursor.close()
            connection.close()
            print('✅ Database connection closed')

if __name__ == '__main__':
    show_products()
