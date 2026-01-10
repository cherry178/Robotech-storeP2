#!/usr/bin/env python3
"""
MySQL Database Setup for Robotech Store
Run this script to create the database and tables
"""

import mysql.connector
from mysql.connector import Error

# Database configuration - Update these with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@123',  # Set your MySQL root password here
    'database': None  # Will create the database first
}

def create_database():
    """Create the robotech_store database"""
    try:
        # Connect without specifying database to create it
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = connection.cursor()

        # Drop database if it exists (to recreate with new schema)
        cursor.execute("DROP DATABASE IF EXISTS robotech_store")
        print("🗑️  Dropped existing 'robotech_store' database")

        # Create database
        cursor.execute("CREATE DATABASE robotech_store")
        print("✅ Database 'robotech_store' created successfully")

        connection.commit()
        cursor.close()
        connection.close()

    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

    return True

def setup_tables():
    """Create all necessary tables"""
    # Update config to include database
    db_config = DB_CONFIG.copy()
    db_config['database'] = 'robotech_store'

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(50) PRIMARY KEY,
                phone VARCHAR(15) UNIQUE NOT NULL,
                email VARCHAR(100),
                name VARCHAR(100),
                address TEXT,
                otp VARCHAR(10),
                logged_in BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Users table created")

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                original_price DECIMAL(10,2),
                category VARCHAR(50),
                subcategory VARCHAR(50),
                image_url VARCHAR(500),
                stock_quantity INT DEFAULT 0,
                is_featured BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Products table created")

        # Create carts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS carts (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id VARCHAR(50),
                product_id INT,
                quantity INT DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE KEY unique_cart_item (user_id, product_id)
            )
        """)
        print("✅ Carts table created")

        connection.commit()

    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

    return True

def insert_demo_data():
    """Insert demo products into the database"""
    db_config = DB_CONFIG.copy()
    db_config['database'] = 'robotech_store'

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] > 0:
            print("ℹ️  Demo data already exists, skipping insertion")
            return True

        # Insert demo products
        demo_products = [
            (1, 'Arduino Uno R3', 'ATmega328P microcontroller board with USB interface', 450.00, 550.00, 'Microcontrollers', 'https://m.media-amazon.com/images/I/51+N-57gSiL.jpg'),
            (2, 'ESP32 Dev Board', 'WiFi & Bluetooth enabled microcontroller for IoT projects', 350.00, 450.00, 'Microcontrollers', 'https://m.media-amazon.com/images/I/61c1D+qVZSL.jpg'),
            (3, 'Raspberry Pi 4', 'Powerful single-board computer for advanced projects', 3500.00, 4200.00, 'Microcontrollers', 'https://m.media-amazon.com/images/I/51R5Q2W6ZSL.jpg'),
            (4, 'Arduino Nano', 'Compact microcontroller board for small projects', 250.00, 300.00, 'Microcontrollers', 'https://m.media-amazon.com/images/I/71vZpqN2TBL.jpg'),
            (5, 'DHT11 Temperature Sensor', 'Digital temperature and humidity sensor', 80.00, 100.00, 'Sensors', 'https://m.media-amazon.com/images/I/61h9xNVXHdL.jpg'),
            (6, 'HC-SR04 Ultrasonic Sensor', 'Distance measuring sensor for robotics', 60.00, 80.00, 'Sensors', 'https://m.media-amazon.com/images/I/71p2N8OMXJL.jpg'),
            (7, 'Servo Motor MG996R', 'High-torque servo motor for robotics', 180.00, 220.00, 'Actuators', 'https://m.media-amazon.com/images/I/61F4Kjdh5FL.jpg'),
            (8, '16x2 LCD Display', 'Character LCD display module', 120.00, 150.00, 'Displays', 'https://m.media-amazon.com/images/I/51BvC6I6XGL.jpg'),
            (9, 'LED Strip 5M', 'RGB LED strip with controller', 200.00, 250.00, 'Displays', 'https://m.media-amazon.com/images/I/61j8VKWkQIL.jpg'),
            (10, 'Breadboard 830 Points', 'Solderless breadboard for prototyping', 90.00, 120.00, 'Tools & Accessories', 'https://m.media-amazon.com/images/I/61W59o8oJZL.jpg')
        ]

        cursor.executemany("""
            INSERT INTO products (id, name, description, price, original_price, category, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, demo_products)

        connection.commit()
        print("✅ Demo products inserted successfully")

    except Error as e:
        print(f"❌ Error inserting demo data: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

    return True

def main():
    """Main setup function"""
    print("🚀 Setting up MySQL database for Robotech Store...")
    print(f"📋 Using MySQL config: {DB_CONFIG['host']} as {DB_CONFIG['user']}")

    # Update password prompt
    if not DB_CONFIG['password']:
        print("⚠️  Please update the password in DB_CONFIG at the top of this file")
        print("   Current password is empty")
        return

    # Create database
    if not create_database():
        return

    # Setup tables
    if not setup_tables():
        return

    # Insert demo data
    if not insert_demo_data():
        return

    print("🎉 MySQL database setup completed successfully!")
    print("📝 Next steps:")
    print("   1. Update DB_CONFIG in backend/app.py with your MySQL credentials")
    print("   2. Run: python backend/app.py")
    print("   3. Your frontend will work unchanged with MySQL backend!")

if __name__ == "__main__":
    main()
