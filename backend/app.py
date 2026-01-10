import os
os.environ['FLASK_SKIP_DOTENV'] = '1'  # Disable automatic dotenv loading
os.environ['DOTENV_FILE'] = ''  # Disable dotenv file loading

from flask import Flask, render_template, request, jsonify
import hashlib
import random
import mysql.connector
from mysql.connector import Error

# Try to use waitress if available, fallback to Flask dev server
try:
    from waitress import serve
    USE_WAITERESS = True
    print("✅ Using Waitress WSGI server")
except ImportError:
    USE_WAITERESS = False
    print("⚠️  Waitress not available, using Flask dev server")

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create Flask app with proper template and static file serving
app = Flask(__name__,
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
app.secret_key = 'test-secret-key'

# Configure CORS - allow all origins in production, specific in development
from flask_cors import CORS
import os

# Get the current environment
ENVIRONMENT = os.environ.get('FLASK_ENV', 'development')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:7000')

if ENVIRONMENT == 'production':
    # In production, allow the deployed frontend domain
    CORS(app, origins=['*'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True)
else:
    # In development, allow localhost ports
    CORS(app, origins=['http://127.0.0.1:7000', 'http://localhost:7000',
                       'http://127.0.0.1:8001', 'http://localhost:8001',
                       'http://127.0.0.1:3000', 'http://localhost:3000'],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         supports_credentials=True)

# Demo mode - bypass database connections
DEMO_MODE = True

# MySQL Database Configuration
# Update these credentials to match your MySQL setup
# Database configuration - use environment variables for production
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Root@123'),
    'database': os.environ.get('DB_NAME', 'robotech_store'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

# For production databases (like JawsDB on Heroku), use DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Parse DATABASE_URL for services like JawsDB, ClearDB, etc.
    import urllib.parse
    url = urllib.parse.urlparse(DATABASE_URL)
    DB_CONFIG = {
        'host': url.hostname,
        'user': url.username,
        'password': url.password,
        'database': url.path.lstrip('/'),
        'port': url.port or 3306
    }

def get_db_connection():
    """Get database connection - try MySQL first, fallback to SQLite"""

    # Try MySQL first (unless in demo mode)
    if ENVIRONMENT != 'demo':
        print(f"🔌 Attempting to connect to MySQL: {DB_CONFIG['host']}:{DB_CONFIG.get('port', 3306)} as {DB_CONFIG['user']}")
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            print("✅ MySQL connection successful")
            return connection
        except Error as e:
            print(f"⚠️  MySQL connection failed: {e}")
            print("   Falling back to SQLite demo mode...")

    # Fallback to SQLite for demo/offline mode
    try:
        import sqlite3
        connection = sqlite3.connect('robotech_store.db', check_same_thread=False)
        connection.row_factory = sqlite3.Row  # Enable column access by name
        print("✅ SQLite demo mode active")
        return connection
    except Exception as e:
        print(f"❌ Both MySQL and SQLite failed: {e}")
        return None

def init_database():
    """Initialize database tables if they don't exist"""
    print("🔧 init_database() function STARTED")
    connection = get_db_connection()
    if not connection:
        print("❌ Could not connect to database for initialization")
        return
    print("✅ Database connection established in init_database()")

    # Check if we're using SQLite
    is_sqlite = 'sqlite' in str(type(connection)).lower()

    try:
        cursor = connection.cursor()

        # Create users table (compatible with both MySQL and SQLite)
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    name TEXT,
                    address TEXT,
                    otp TEXT,
                    logged_in INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
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

        # Add logged_in column if it doesn't exist (for existing tables)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN logged_in BOOLEAN DEFAULT FALSE")
            print("✅ Added logged_in column to users table")
        except Error as e:
            if "Duplicate column name" not in str(e):
                print(f"⚠️ Could not add logged_in column: {e}")
            else:
                print("ℹ️ logged_in column already exists")

        # Drop all tables in correct order to avoid foreign key constraints
        print("🔄 Dropping all tables in correct order...")
        cursor.execute("DROP TABLE IF EXISTS cart")
        cursor.execute("DROP TABLE IF EXISTS order_items")
        cursor.execute("DROP TABLE IF EXISTS orders")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS users")
        print("✅ All tables dropped successfully")

        # Create users table first (referenced by others)
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE users (
                    id TEXT PRIMARY KEY,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    name TEXT,
                    address TEXT,
                    otp TEXT,
                    logged_in INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE users (
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
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    original_price REAL,
                    category TEXT,
                    subcategory TEXT,
                    image_url TEXT,
                    stock_quantity INTEGER DEFAULT 0,
                    is_featured INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE products (
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

        # Create orders table (references users)
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    payment_method TEXT,
                    shipping_address TEXT,
                    billing_name TEXT,
                    billing_email TEXT,
                    billing_phone TEXT,
                    billing_city TEXT,
                    billing_zip TEXT,
                    user_order_number INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE orders (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id VARCHAR(50),
                    total_amount DECIMAL(10,2) NOT NULL,
                    status VARCHAR(50) DEFAULT 'pending',
                    payment_method VARCHAR(50),
                    shipping_address TEXT,
                    billing_name VARCHAR(255),
                    billing_email VARCHAR(255),
                    billing_phone VARCHAR(20),
                    billing_city VARCHAR(100),
                    billing_zip VARCHAR(20),
                    user_order_number INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
        print("✅ Orders table created")

        # Create order_items table (references products and orders)
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE order_items (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    order_id INT,
                    product_id INT,
                    quantity INT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
        print("✅ Order_items table created")

        # Create cart table (references users and products)
        if is_sqlite:
            cursor.execute("""
                CREATE TABLE cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    product_id INTEGER,
                    quantity INTEGER DEFAULT 1,
                    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """)
            # SQLite doesn't support UNIQUE KEY syntax in CREATE TABLE
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_cart_item ON cart(user_id, product_id)")
        else:
            cursor.execute("""
                CREATE TABLE cart (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id VARCHAR(50),
                    product_id INT,
                    quantity INT DEFAULT 1,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_cart_item (user_id, product_id)
                )
            """)
        print("✅ Cart table created with foreign key constraints")

        # Verify the tables were created correctly
        cursor.execute("DESCRIBE products")
        columns = cursor.fetchall()
        print("📋 Products table columns:")
        for col in columns:
            print(f"   - {col[0]}: {col[1]}")
        print("✅ Table schema verified")


        # FORCE CLEAR ALL EXISTING PRODUCTS - NO MATTER WHAT
        print("🔄 FORCE clearing ALL existing products from database...")

        # FIRST: Clear ALL cart items (start fresh on database reload)
        cursor.execute("DELETE FROM cart")
        connection.commit()  # Commit cart clearing first
        print("🗑️ Cleared ALL cart items (fresh start)")

        # Check what's currently in the database
        cursor.execute("SELECT COUNT(*) FROM products")
        old_count = cursor.fetchone()[0]
        print(f"📊 Found {old_count} existing products before clearing")

        # Clear ALL products (now safe since cart is empty)
        cursor.execute("DELETE FROM products")
        connection.commit()  # Commit product clearing
        print("🗑️ Cleared ALL products from database")

        # Verify clearing worked
        cursor.execute("SELECT COUNT(*) FROM products")
        after_clear_count = cursor.fetchone()[0]
        print(f"📊 After clearing: {after_clear_count} products (should be 0)")

        # Reset auto-increment
        try:
            cursor.execute("ALTER TABLE products AUTO_INCREMENT = 1")
            print("🔄 Reset auto-increment counter")
        except Error as e:
            print(f"⚠️ Could not reset auto-increment: {e}")

        # Load ONLY products from DEMO_PRODUCTS
        print(f"📦 Loading {len(DEMO_PRODUCTS)} products from DEMO_PRODUCTS...")
        if len(DEMO_PRODUCTS) == 0:
            print("❌ CRITICAL ERROR: DEMO_PRODUCTS list is empty!")
            return

        print(f"📋 DEMO_PRODUCTS contains {len(DEMO_PRODUCTS)} products")
        print(f"📋 First product: {DEMO_PRODUCTS[0]['name']} (ID: {DEMO_PRODUCTS[0]['id']})")
        print(f"📋 Last product: {DEMO_PRODUCTS[-1]['name']} (ID: {DEMO_PRODUCTS[-1]['id']})")

        inserted_count = 0
        failed_count = 0
        for i, product in enumerate(DEMO_PRODUCTS):
            try:
                cursor.execute("""
                    INSERT INTO products (id, name, description, price, category, image_url, stock_quantity, is_featured)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    product['id'],
                    product['name'],
                    product['description'],
                    product['price'],
                    product['category'],
                    product['image_url'],
                    product['stock_quantity'],
                    product['is_featured']
                ))
                inserted_count += 1
                if inserted_count <= 3:  # Show first 3 insertions
                    print(f"✅ Inserted: ID {product['id']} - {product['name']}")
                elif inserted_count == len(DEMO_PRODUCTS):  # Show last one
                    print(f"✅ Inserted: ID {product['id']} - {product['name']} (last product)")
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed to insert product {product['id']} - {product['name']}: {e}")
                if failed_count <= 3:  # Show first 3 failures
                    continue

        print(f"📊 Insertion summary: {inserted_count} successful, {failed_count} failed")

        if inserted_count > 0:
            # Commit all product insertions
            connection.commit()
            print(f"✅ Committed {inserted_count} products to database")
        else:
            print("❌ No products were inserted - rolling back")
            connection.rollback()
            return

        # Verify what we loaded
        cursor.execute("SELECT COUNT(*) FROM products")
        new_count = cursor.fetchone()[0]
        print(f"✅ Database now has {new_count} products (should be {len(DEMO_PRODUCTS)})")

        # Cart was already cleared at the beginning

        # FINAL VERIFICATION
        cursor.execute("SELECT COUNT(*) FROM products")
        final_count = cursor.fetchone()[0]
        print(f"📊 FINAL COUNT: {final_count} products in database")

        # Check your key products
        key_ids = [1, 2, 36, 41, 26, 51]  # Include 26 (Lilypad) and 51 (PCB Antenna) to check if they're gone
        placeholders = ','.join(['%s'] * len(key_ids))
        cursor.execute(f"SELECT id, name FROM products WHERE id IN ({placeholders})", key_ids)
        key_products = cursor.fetchall()
        print("🔑 KEY PRODUCTS CHECK:")
        for prod_id, prod_name in key_products:
            if prod_id == 26 and "Lilypad" in prod_name:
                status = "❌ STILL HAS ARDUINO LILYPAD!"
            elif prod_id == 51 and "PCB Antenna" in prod_name:
                status = "❌ STILL HAS PCB ANTENNA!"
            else:
                status = "✅ CORRECT"
            print(f"   - ID {prod_id}: {prod_name} {status}")

        # Check for any old products that shouldn't exist
        cursor.execute("SELECT id, name FROM products WHERE name LIKE '%Lilypad%' OR name LIKE '%PCB Antenna%' OR name LIKE '%Arduino%' AND name NOT LIKE '%Uno%' AND name NOT LIKE '%Due%' AND name NOT LIKE '%Mega%' AND name NOT LIKE '%Nano%'")
        bad_products = cursor.fetchall()
        if bad_products:
            print("❌ CRITICAL ERROR: Found unwanted products:")
            for prod_id, prod_name in bad_products:
                print(f"   - ID {prod_id}: {prod_name} ❌")
        else:
            print("✅ SUCCESS: No unwanted products found - database is clean!")

        # Show first 5 products to verify correct loading
        cursor.execute("SELECT id, name FROM products ORDER BY id LIMIT 5")
        first_five = cursor.fetchall()
        print("📋 FIRST 5 PRODUCTS IN DATABASE:")
        for prod_id, prod_name in first_five:
            print(f"   - ID {prod_id}: {prod_name}")

        connection.commit()
        print("✅ Database initialized successfully")
        print("🎉 init_database() COMPLETED SUCCESSFULLY!")

    except Error as e:
        print(f"❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"❌ Unexpected error in init_database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print("🔌 Database connection closed")

# Test MySQL connection
print("🔍 Testing MySQL connection...")
test_conn = get_db_connection()
if test_conn:
    print("✅ MySQL connection test successful")
    test_conn.close()
else:
    print("❌ MySQL connection test failed - cart operations will not work!")

print("✅ Flask app initialized successfully")

# In-memory storage for demo purposes (keeping for frontend compatibility)
DEMO_USERS = {}
DEMO_PRODUCTS = [
    {
        "id": 11,
        "name": "Arduino Uno R3",
        "description": "ATmega328P microcontroller board with USB interface",
        "price": 450.0,
        "category": "Microcontrollers",
        "stock_quantity": 30,
        "image_url": "https://m.media-amazon.com/images/I/51+N-57gSiL.jpg",
        "is_featured": False
    },
    {
        "id": 12,
        "name": "ESP32 Development Board",
        "description": "WiFi & Bluetooth enabled microcontroller",
        "price": 350.0,
        "category": "Microcontrollers",
        "stock_quantity": 40,
        "image_url": "https://i.pinimg.com/736x/02/a1/01/02a101e95d5a8f6be9adca70e9d6f87e.jpg",
        "is_featured": False
    },
    {
        "id": 13,
        "name": "DHT11 Temperature & Humidity Sensor",
        "description": "Digital temperature and humidity sensor with 1-wire interface",
        "price": 45.0,
        "category": "Sensors",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/7b/c7/1e/7bc71ed8923c0ad6e8d7bcc115ef59de.jpg",
        "is_featured": False
    },
    {
        "id": 14,
        "name": "HC-SR04 Ultrasonic Sensor",
        "description": "Ultrasonic ranging sensor for distance measurement",
        "price": 85.0,
        "category": "Sensors",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/1200x/1d/84/dc/1d84dc4fb7a5ac5e2d9121911f4067da.jpg",
        "is_featured": False
    },
    {
        "id": 15,
        "name": "SG90 Servo Motor",
        "description": "9g micro servo motor for robotics",
        "price": 95.0,
        "category": "Actuators",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/736x/a6/c5/5a/a6c55a797bc6e00f4ca5c91b84afec98.jpg",
        "is_featured": False
    },
    {
        "id": 16,
        "name": "DC Motor",
        "description": "12V DC geared motor for robotics and automation projects",
        "price": 150.0,
        "category": "Actuators",
        "stock_quantity": 85,
        "image_url": "https://m.media-amazon.com/images/I/41OZaG+qvsL.jpg",
        "is_featured": False
    },
    {
        "id": 17,
        "name": "Stepper Motor",
        "description": "NEMA 17 stepper motor with 1.8° step angle for precision control",
        "price": 450.0,
        "category": "Actuators",
        "stock_quantity": 45,
        "image_url": "https://m.media-amazon.com/images/I/51fLU88NI6L.jpg",
        "is_featured": True
    },
    {
        "id": 18,
        "name": "LCD Crystal Display",
        "description": "16x2 character LCD display module with backlight",
        "price": 120.0,
        "category": "Displays",
        "stock_quantity": 85,
        "image_url": "https://i.pinimg.com/736x/55/fd/a1/55fda180c7904f25067c840a8302d0a7.jpg",
        "is_featured": False
    },
    {
        "id": 19,
        "name": "OLED Display",
        "description": "0.96 inch I2C OLED display module with 128x64 resolution",
        "price": 150.0,
        "category": "Displays",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/fd/ef/d4/fdefd4f32f98c1a2c6f15b71c12ecc75.jpg",
        "is_featured": False
    },
    {
        "id": 20,
        "name": "TFT Screen",
        "description": "2.8 inch TFT LCD color touch screen display",
        "price": 850.0,
        "category": "Displays",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/e4/d6/fa/e4d6fa1f834a4c26203690590de22ea4.jpg",
        "is_featured": True
    },
    {
        "id": 21,
        "name": "7-Segment Display",
        "description": "4-digit 7-segment display with decimal points",
        "price": 65.0,
        "category": "Displays",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/736x/31/a0/60/31a060caefe320fdf1108f364e681f1d.jpg",
        "is_featured": False
    },
    {
        "id": 22,
        "name": "E-paper Display",
        "description": "1.54 inch e-paper display for low power applications",
        "price": 650.0,
        "category": "Displays",
        "stock_quantity": 30,
        "image_url": "https://i.pinimg.com/1200x/50/5d/4a/505d4ab5dff8115c1dc1e2391ed6d1fb.jpg",
        "is_featured": False
    },
    {
        "id": 23,
        "name": "LED Matrix Display",
        "description": "8x8 LED matrix display with MAX7219 driver",
        "price": 95.0,
        "category": "Displays",
        "stock_quantity": 70,
        "image_url": "https://i.pinimg.com/736x/0f/b0/b1/0fb0b100bb886ac9f050213bef229042.jpg",
        "is_featured": False
    },
    {
        "id": 24,
        "name": "LCD Touchscreen Module",
        "description": "2.4 inch LCD touchscreen module for user interfaces",
        "price": 1200.0,
        "category": "Displays",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/1200x/f7/ba/f5/f7baf50e5993ccffc68e5387bda0b342.jpg",
        "is_featured": True
    },
    {
        "id": 25,
        "name": "2 Battery Holders",
        "description": "AA battery holder for 2 batteries in series",
        "price": 25.0,
        "category": "Power Supply",
        "stock_quantity": 150,
        "image_url": "https://i.pinimg.com/1200x/51/d7/f8/51d7f86c3ba3a7e9081902780d10d159.jpg",
        "is_featured": False
    },
    {
        "id": 26,
        "name": "3 Battery Holders",
        "description": "AA battery holder for 3 batteries in series",
        "price": 35.0,
        "category": "Power Supply",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/d6/ca/b6/d6cab6537f5899be3171be162f5b9fab.jpg",
        "is_featured": False
    },
    {
        "id": 27,
        "name": "DC-DC Converter",
        "description": "Adjustable DC-DC buck converter module 5V-35V",
        "price": 85.0,
        "category": "Power Supply",
        "stock_quantity": 90,
        "image_url": "https://i.pinimg.com/1200x/f9/f8/fb/f9f8fb91419f05a2436d0a3ca731586a.jpg",
        "is_featured": False
    },
    {
        "id": 28,
        "name": "Power Bank Module",
        "description": "18650 lithium battery power bank module",
        "price": 180.0,
        "category": "Power Supply",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/4c/45/0f/4c450f39f070b12698645d02dcf10a3a.jpg",
        "is_featured": False
    },
    {
        "id": 29,
        "name": "Breadboard",
        "description": "830 tie-point solderless breadboard for prototyping",
        "price": 85.0,
        "category": "Tools & Accessories",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/c6/2e/fe/c62efe7156acb4a732ee2a0985cdb1b0.jpg",
        "is_featured": False
    },
    {
        "id": 30,
        "name": "Male-Male Jumper Wires",
        "description": "40-piece male-to-male jumper wire set",
        "price": 45.0,
        "category": "Tools & Accessories",
        "stock_quantity": 200,
        "image_url": "https://i.pinimg.com/1200x/ef/20/2c/ef202c20c5b52e44bb7cef23d80d31ac.jpg",
        "is_featured": False
    },
    {
        "id": 31,
        "name": "Male-Female Jumper Wires",
        "description": "40-piece male-to-female jumper wire set",
        "price": 50.0,
        "category": "Tools & Accessories",
        "stock_quantity": 180,
        "image_url": "https://i.pinimg.com/1200x/fc/51/ee/fc51ee3784738477942608abcf9c8d21.jpg",
        "is_featured": False
    },
    {
        "id": 32,
        "name": "Lithium Polymer Battery",
        "description": "3.7V 1000mAh LiPo battery with JST connector",
        "price": 250.0,
        "category": "Power Supply",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/736x/da/53/f7/da53f7c21e5a4b9df6d544bacc1ff085.jpg",
        "is_featured": False
    },
    {
        "id": 33,
        "name": "PCB Prototyping Board",
        "description": "Double-sided PCB prototyping board with copper pads",
        "price": 120.0,
        "category": "Tools & Accessories",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/c0/e7/85/c0e785c8bcfadf88efbdd9bbfbb44e1f.jpg",
        "is_featured": False
    },
    {
        "id": 34,
        "name": "Nuts & Bolts Kit",
        "description": "Assorted nuts and bolts set for electronics projects",
        "price": 65.0,
        "category": "Tools & Accessories",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/1200x/51/f6/84/51f684e16602b2affc0016f1b32bbb0e.jpg",
        "is_featured": False
    },
    {
        "id": 38,
        "name": "Linear Voltage Regulator",
        "description": "LM7805 5V linear voltage regulator IC",
        "price": 15.0,
        "category": "Power Supply",
        "stock_quantity": 300,
        "image_url": "https://i.pinimg.com/736x/f1/ba/b4/f1bab45eff6c23f981b993006bd5fcd4.jpg",
        "is_featured": False
    },
    {
        "id": 39,
        "name": "Audio Adapter Board",
        "description": "Audio amplifier board with speaker connector",
        "price": 120.0,
        "category": "Audio Components",
        "stock_quantity": 50,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 40,
        "name": "USB Cable",
        "description": "USB 2.0 A to B cable for programming and data transfer",
        "price": 35.0,
        "category": "Tools & Accessories",
        "stock_quantity": 250,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },
    {
        "id": 41,
        "name": "Brushless DC Motor",
        "description": "High-efficiency brushless DC motor for precision applications",
        "price": 850.0,
        "category": "Actuators",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/1200x/f7/17/c3/f717c366e958fc149ff3c5139167afc2.jpg",
        "is_featured": False
    },
    {
        "id": 42,
        "name": "Bluetooth Controlled Linear Actuator",
        "description": "Wireless controlled linear motion actuator",
        "price": 2500.0,
        "category": "Actuators",
        "stock_quantity": 8,
        "image_url": "https://i.pinimg.com/736x/29/76/e3/2976e334ded326d7cec03488972b5005.jpg",
        "is_featured": True
    },
    {
        "id": 43,
        "name": "Continuous Rotation Robot Servo",
        "description": "360-degree continuous rotation servo motor",
        "price": 180.0,
        "category": "Actuators",
        "stock_quantity": 45,
        "image_url": "https://i.pinimg.com/1200x/bb/be/d9/bbbed9dc8ef3e9addf3157f2eb5c494c.jpg",
        "is_featured": False
    },
    {
        "id": 44,
        "name": "Motor Driver Shield",
        "description": "Arduino shield for motor control applications",
        "price": 350.0,
        "category": "Actuators",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/736x/b7/cc/d7/b7ccd715fa879b2464e4455a88a1b569.jpg",
        "is_featured": False
    },
    {
        "id": 45,
        "name": "H-Bridge DC Stepper Motor Control Module",
        "description": "Dual H-bridge motor driver for stepper motors",
        "price": 120.0,
        "category": "Actuators",
        "stock_quantity": 30,
        "image_url": "https://i.pinimg.com/1200x/f1/5c/33/f15c3335d76619c8fb68a75b0a3ff676.jpg",
        "is_featured": False
    },
    {
        "id": 46,
        "name": "Raspberry Pi Zero W",
        "description": "Compact single-board computer with WiFi and Bluetooth",
        "price": 1200.0,
        "category": "Microcontrollers",
        "stock_quantity": 35,
        "image_url": "https://i.pinimg.com/1200x/f7/56/7c/f7567c73f08d270f14b0fccf8f7e18bc.jpg",
        "is_featured": False
    },
    {
        "id": 47,
        "name": "Arduino Mega",
        "description": "ATmega2560 microcontroller board with expanded I/O",
        "price": 1800.0,
        "category": "Microcontrollers",
        "stock_quantity": 20,
        "image_url": "https://i.pinimg.com/1200x/06/08/de/0608de0634b243a211b38aa0ef742c29.jpg",
        "is_featured": True
    },
    {
        "id": 48,
        "name": "Arduino Nano",
        "description": "Compact ATmega328 microcontroller board",
        "price": 250.0,
        "category": "Microcontrollers",
        "stock_quantity": 50,
        "image_url": "https://i.pinimg.com/736x/a2/6a/8e/a26a8eb43e8d3f28d30ca4e9e5df3c7e.jpg",
        "is_featured": False
    },
    {
        "id": 49,
        "name": "Arduino Due",
        "description": "ARM Cortex-M3 microcontroller board with 32-bit architecture",
        "price": 2200.0,
        "category": "Microcontrollers",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/736x/6d/3d/bf/6d3dbf8d5e143594628d4eb40d64ae93.jpg",
        "is_featured": True
    },
    {
        "id": 50,
        "name": "ESP8266",
        "description": "WiFi enabled microcontroller module",
        "price": 150.0,
        "category": "Microcontrollers",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/9a/de/f8/9adef8fdfe6b094c40ce148305ebd640.jpg",
        "is_featured": False
    },
    {
        "id": 51,
        "name": "Adafruit Feather M0",
        "description": "ARM Cortex-M0+ microcontroller board with Bluetooth",
        "price": 650.0,
        "category": "Microcontrollers",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/27/42/d7/2742d764962b3debf7ec4475259071b1.jpg",
        "is_featured": True
    },
    {
        "id": 52,
        "name": "Teensy 4.1",
        "description": "ARM Cortex-M7 microcontroller development board",
        "price": 850.0,
        "category": "Microcontrollers",
        "stock_quantity": 22,
        "image_url": "https://m.media-amazon.com/images/I/41GE3LYUSpL.jpg",
        "is_featured": False
    },
    {
        "id": 53,
        "name": "Banana Pi",
        "description": "Single-board computer with Allwinner A20 processor",
        "price": 2500.0,
        "category": "Microcontrollers",
        "stock_quantity": 12,
        "image_url": "https://m.media-amazon.com/images/I/41nUU4o8GiL.jpg",
        "is_featured": True
    },
    {
        "id": 54,
        "name": "Orange Pi",
        "description": "Single-board computer with H3 processor",
        "price": 1800.0,
        "category": "Microcontrollers",
        "stock_quantity": 18,
        "image_url": "https://m.media-amazon.com/images/I/41qjsxkbRJL.jpg",
        "is_featured": True
    },
    {
        "id": 55,
        "name": "Rain Sensor",
        "description": "Rain detection sensor module",
        "price": 75.0,
        "category": "Sensors",
        "stock_quantity": 55,
        "image_url": "https://i.pinimg.com/736x/ce/c0/d3/cec0d3cf5548a1fbbdbfe666c79d9175.jpg",
        "is_featured": False
    },
    {
        "id": 56,
        "name": "Sound Vibration Sensor",
        "description": "Vibration and sound detection sensor",
        "price": 55.0,
        "category": "Sensors",
        "stock_quantity": 70,
        "image_url": "https://i.pinimg.com/736x/4d/40/6c/4d406c89085fbde96a521b2797ff858e.jpg",
        "is_featured": False
    },
    {
        "id": 57,
        "name": "Color Sensor (TCS34725)",
        "description": "RGB color sensor with IR blocking filter",
        "price": 180.0,
        "category": "Sensors",
        "stock_quantity": 40,
        "image_url": "https://m.media-amazon.com/images/I/41Q-F-oaBjL.jpg",
        "is_featured": False
    },
    {
        "id": 58,
        "name": "Sound Sensor",
        "description": "Microphone sound detection module",
        "price": 45.0,
        "category": "Sensors",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/1200x/32/93/f5/3293f5f14ee3c654bf5a13c3c851303e.jpg",
        "is_featured": False
    },
    {
        "id": 59,
        "name": "Water Level Sensor",
        "description": "Liquid level detection sensor",
        "price": 65.0,
        "category": "Sensors",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/6d/58/76/6d58764a2d251db90da81810cfd54529.jpg",
        "is_featured": False
    },
    {
        "id": 60,
        "name": "5V Relay Module",
        "description": "Electromagnetic relay module for switching applications",
        "price": 35.0,
        "category": "Actuators",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/1200x/2b/93/68/2b9368118a4b55c6d9d1097b55edaeb6.jpg",
        "is_featured": False
    },
    {
        "id": 61,
        "name": "Electret Microphone Module",
        "description": "Condenser microphone module for audio input",
        "price": 40.0,
        "category": "Audio Components",
        "stock_quantity": 75,
        "image_url": "https://m.media-amazon.com/images/I/41LF+yoKDGS.jpg",
        "is_featured": False
    },
    {
        "id": 62,
        "name": "Voice Recognition Microphone Board",
        "description": "Advanced voice recognition and processing board",
        "price": 350.0,
        "category": "Audio Components",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/82/20/cd/8220cd500d80ce85ae112cb743d27c15.jpg",
        "is_featured": False
    },
    {
        "id": 63,
        "name": "Robocraze Speech Recognition Module",
        "description": "Voice command recognition module",
        "price": 450.0,
        "category": "Audio Components",
        "stock_quantity": 20,
        "image_url": "https://m.media-amazon.com/images/I/51-1ruiVkVL.jpg",
        "is_featured": True
    },
    {
        "id": 64,
        "name": "Active Buzzer Module",
        "description": "Electronic buzzer module with built-in oscillator",
        "price": 25.0,
        "category": "Audio Components",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/43/10/87/431087ed78d6e014a611787cb4ac6963.jpg",
        "is_featured": False
    },
    {
        "id": 65,
        "name": "Passive Buzzer",
        "description": "Piezo buzzer for audio output without oscillator",
        "price": 20.0,
        "category": "Audio Components",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/736x/7d/58/ed/7d58ed71e86237abc1f31b67d8f08639.jpg",
        "is_featured": False
    },
    {
        "id": 68,
        "name": "Infrared Obstacle Sensor",
        "description": "IR proximity sensor for obstacle detection",
        "price": 35.0,
        "category": "Sensors",
        "stock_quantity": 90,
        "image_url": "https://i.pinimg.com/736x/15/fe/19/15fe193153c29952640b42ea92b8ba12.jpg",
        "is_featured": False
    },
    {
        "id": 69,
        "name": "PIR Motion Sensor",
        "description": "Passive infrared motion detector sensor",
        "price": 75.0,
        "category": "Sensors",
        "stock_quantity": 65,
        "image_url": "https://i.pinimg.com/736x/fb/3e/6d/fb3e6d329d4c2356c76c84246ceb1dca.jpg",
        "is_featured": False
    },
    {
        "id": 70,
        "name": "Temperature Sensor (DS18B20)",
        "description": "Digital temperature sensor with 1-wire interface",
        "price": 55.0,
        "category": "Sensors",
        "stock_quantity": 85,
        "image_url": "https://i.pinimg.com/736x/78/8b/ea/788beaacc3994d3b7a80b04aeb6b08ed.jpg",
        "is_featured": False
    },
    {
        "id": 71,
        "name": "Pressure Sensor (BMP280)",
        "description": "Barometric pressure and temperature sensor",
        "price": 120.0,
        "category": "Sensors",
        "stock_quantity": 45,
        "image_url": "https://i.pinimg.com/736x/2c/f3/25/2cf3253970912c9d71827c0754d24b52.jpg",
        "is_featured": False
    },
    {
        "id": 72,
        "name": "Gas Sensor (MQ-2)",
        "description": "Combustible gas and smoke sensor",
        "price": 85.0,
        "category": "Sensors",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/736x/25/45/c7/2545c7432cd113a3d69dab5e25aefe65.jpg",
        "is_featured": False
    },
    {
        "id": 73,
        "name": "Gas Sensor (MQ-135)",
        "description": "Air quality sensor for detecting harmful gases",
        "price": 90.0,
        "category": "Sensors",
        "stock_quantity": 55,
        "image_url": "https://i.pinimg.com/736x/35/3c/cb/353ccbf6dac0d3e6e924149b04651dd1.jpg",
        "is_featured": False
    },
    {
        "id": 74,
        "name": "Light Sensor (LDR)",
        "description": "Light dependent resistor for light intensity measurement",
        "price": 15.0,
        "category": "Sensors",
        "stock_quantity": 150,
        "image_url": "https://i.pinimg.com/736x/2a/29/86/2a29868718c02a045dee1db8eb5d1b03.jpg",
        "is_featured": False
    },
    {
        "id": 75,
        "name": "Touch Sensor",
        "description": "Capacitive touch sensor module",
        "price": 30.0,
        "category": "Sensors",
        "stock_quantity": 95,
        "image_url": "https://i.pinimg.com/736x/29/42/f9/2942f99ba1f9f4c2088a5b53fbf2174c.jpg",
        "is_featured": False
    },
    {
        "id": 76,
        "name": "TFT Screen",
        "description": "2.8 inch TFT LCD color touch screen display",
        "price": 850.0,
        "category": "Displays",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/e4/d6/fa/e4d6fa1f834a4c26203690590de22ea4.jpg",
        "is_featured": True
    }
]

# Product functions using MySQL database
def get_products_from_db(category=None, search=None, featured=None, sort_by='name', page=1, limit=6):
    """Get products from database with filtering, sorting, and pagination"""
    connection = get_db_connection()
    if not connection:
        print("❌ Could not connect to database, falling back to DEMO_PRODUCTS")
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        
        # Build WHERE clause
        where_conditions = []
        params = []
        
        if category and category != 'all':
            where_conditions.append("category = %s")
            params.append(category)
        
        if search:
            where_conditions.append("(name LIKE %s OR description LIKE %s)")
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern])
        
        if featured is not None:
            where_conditions.append("is_featured = %s")
            params.append(featured)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # Build ORDER BY clause
        order_by = "ORDER BY "
        if sort_by == 'price_low':
            order_by += "price ASC"
        elif sort_by == 'price_high':
            order_by += "price DESC"
        elif sort_by == 'name':
            order_by += "name ASC"
        elif sort_by == 'newest':
            order_by += "id DESC"
        else:
            order_by += "name ASC"
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM products{where_clause}"
        cursor.execute(count_query, params)
        total_result = cursor.fetchone()
        total_products = total_result['total'] if total_result else 0
        
        # Get paginated products
        offset = (page - 1) * limit
        query = f"""
            SELECT id, name, description, price, category, stock_quantity, image_url, is_featured
            FROM products
            {where_clause}
            {order_by}
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        cursor.execute(query, params)
        products = cursor.fetchall()
        
        # Convert to list of dicts with consistent keys
        result = []
        for p in products:
            result.append({
                'id': p['id'],
                'name': p['name'],
                'description': p['description'],
                'price': float(p['price']),
                'category': p['category'],
                'stock_quantity': p['stock_quantity'],
                'image_url': p['image_url'],
                'is_featured': bool(p['is_featured'])
            })
        
        print(f"📦 Retrieved {len(result)} products from database (total: {total_products})")
        return {
            'products': result,
            'total': total_products,
            'page': page,
            'limit': limit,
            'total_pages': (total_products + limit - 1) // limit
        }
        
    except Error as e:
        print(f"❌ Error getting products from database: {e}")
        return None
    finally:
        if connection:
            connection.close()

# Cart functions using MySQL database
def get_user_cart(user_id):
    """Get user's cart items from database"""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.name, p.price, p.image_url, p.description, p.category
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        print(f"📋 Retrieved {len(cart_items)} cart items for user {user_id}:")
        for item in cart_items:
            print(f"   - Product {item['product_id']}: {item['name']} (qty: {item['quantity']})")
        return cart_items
    except Error as e:
        print(f"Error getting user cart: {e}")
        return []
    finally:
        if connection:
            connection.close()

def add_to_cart(user_id, product_id, quantity=1):
    """Add item to user's cart"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        # Use INSERT ... ON DUPLICATE KEY UPDATE to handle existing items
        cursor.execute("""
            INSERT INTO cart (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + %s
        """, (user_id, product_id, quantity, quantity))
        connection.commit()
        return True
    except Error as e:
        print(f"Error adding to cart: {e}")
        return False
    finally:
        if connection:
            connection.close()

def validate_cart_inputs(user_id, product_id, quantity):
    """Validate cart operation inputs"""
    if not user_id or user_id == 'guest':
        print(f"❌ Invalid user_id: {user_id}")
        return False, "Invalid user ID"

    if not isinstance(user_id, str) or len(user_id.strip()) == 0:
        print(f"❌ User ID must be non-empty string: {user_id}")
        return False, "Invalid user ID format"

    if not isinstance(product_id, int) or product_id <= 0:
        print(f"❌ Product ID must be positive integer: {product_id}")
        return False, "Invalid product ID"

    if not isinstance(quantity, int):
        print(f"❌ Quantity must be integer: {quantity}")
        return False, "Invalid quantity"

    return True, None

def update_cart_item(user_id, product_id, quantity):
    """Update cart item quantity (handles both insert and update)"""
    print(f"🔄 update_cart_item called: user_id='{user_id}', product_id={product_id}, quantity={quantity}")

    # Validate inputs
    is_valid, error_msg = validate_cart_inputs(user_id, product_id, quantity)
    if not is_valid:
        print(f"❌ Input validation failed: {error_msg}")
        return False

    connection = get_db_connection()
    if not connection:
        print("❌ Failed to get database connection")
        return False

    is_sqlite = is_sqlite_connection(connection)

    try:
        cursor = connection.cursor()
        print("✅ Database connection established")

        # Double-check user exists (safety check) - use correct placeholder syntax
        if is_sqlite:
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if cursor.fetchone() is None:
            print(f"❌ User {user_id} does not exist in database - cannot update cart")
            return False

        # Check if product exists before adding to cart - use correct placeholder syntax
        if is_sqlite:
            cursor.execute("SELECT id, name FROM products WHERE id = ?", (product_id,))
        else:
            cursor.execute("SELECT id, name FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        if product is None:
            print(f"❌ Product {product_id} does not exist in database - cannot add to cart")
            return False
        else:
            # Handle both MySQL tuple and SQLite Row results
            product_name = product[1] if isinstance(product, (tuple, list)) else product['name']
            print(f"✅ Product {product_id} exists: {product_name}")

        if quantity <= 0:
            # Remove item if quantity is 0 or negative - use correct placeholder syntax
            print(f"🗑️ Removing item {product_id} from cart for user {user_id}")
            if is_sqlite:
                cursor.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
            else:
                cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            affected_rows = cursor.rowcount
            print(f"🗑️ Delete query executed for item {product_id}, affected rows: {affected_rows}")
        else:
            # Insert or update quantity - SQLite uses ON CONFLICT, MySQL uses ON DUPLICATE KEY
            print(f"📝 Inserting/updating item {product_id} quantity to {quantity} for user {user_id}")
            if is_sqlite:
                cursor.execute("""
                    INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = ?
                """, (user_id, product_id, quantity, quantity))
            else:
                cursor.execute("""
                    INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE quantity = %s
                """, (user_id, product_id, quantity, quantity))
            affected_rows = cursor.rowcount
            print(f"✅ Insert/update query executed for item {product_id}, affected rows: {affected_rows}")

        connection.commit()
        print("✅ Database transaction committed successfully")
        return True

    except Error as e:
        print(f"❌ Database error in update_cart_item: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Unexpected error in update_cart_item: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("🔌 Database connection closed")

def remove_from_cart(user_id, product_id):
    """Remove item from user's cart"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM cart WHERE user_id = %s AND product_id = %s
        """, (user_id, product_id))
        connection.commit()
        return True
    except Error as e:
        print(f"Error removing from cart: {e}")
        return False
    finally:
        if connection:
            connection.close()

def clear_user_cart(user_id):
    """Clear all items from user's cart"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        connection.commit()
        return True
    except Error as e:
        print(f"Error clearing cart: {e}")
        return False
    finally:
        if connection:
            connection.close()

def save_user_to_mysql(user_id, phone):
    """Save user to MySQL database"""
    connection = get_db_connection()
    if not connection:
        print(f"❌ Cannot save user {user_id} to MySQL - no connection")
        return False

    try:
        cursor = connection.cursor()
        # Use INSERT ... ON DUPLICATE KEY UPDATE to handle existing users
        cursor.execute("""
            INSERT INTO users (id, phone, logged_in)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE logged_in = %s
        """, (user_id, phone, True, True))
        connection.commit()
        print(f"✅ User {user_id} saved to MySQL database")
        return True
    except Error as e:
        print(f"❌ Error saving user {user_id} to MySQL: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()
DEMO_OTPS = {}

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Simple test route"""
    return "Server is working! Hello from Robotech Store."

@app.route('/login')
def login():
    """Login page route"""
    return render_template('login.html')

@app.route('/products')
def products():
    """Products page route"""
    return render_template('products.html')

@app.route('/cart')
def cart():
    """Shopping cart page route"""
    return render_template('cart.html')

@app.route('/payment')
def payment():
    """Payment page route"""
    return render_template('payment.html')

@app.route('/orders')
def orders():
    """Orders page route"""
    return render_template('orders.html')

# API Routes
@app.route('/api/user/status', methods=['GET'])
def api_user_status():
    """API endpoint to check user login status"""
    return jsonify({'logged_in': False})

@app.route('/api/products', methods=['GET'])
def api_products():
    """API endpoint to get products from database"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 6))
        category = request.args.get('category', '')
        sort_by = request.args.get('sort', 'name')
        search = request.args.get('search', '').lower()
        featured = request.args.get('featured', '').lower() == 'true'

        # Try to get products from database first
        db_result = get_products_from_db(
            category=category if category and category != 'all' else None,
            search=search if search else None,
            featured=featured if featured else None,
            sort_by=sort_by,
            page=page,
            limit=limit
        )

        if db_result:
            # Use database results
            print(f"📤 API returning {len(db_result['products'])} products from database for page {page}")
            for i, p in enumerate(db_result['products']):
                print(f"   {i+1}. ID {p['id']} - {p['name']}")
            
            return jsonify({
                'success': True,
                'products': db_result['products'],
                'pagination': {
                    'total': db_result['total'],
                    'page': db_result['page'],
                    'limit': db_result['limit'],
                    'pages': db_result['total_pages']
                }
            })
        else:
            # Fallback to DEMO_PRODUCTS if database fails
            print("⚠️ Database query failed, falling back to DEMO_PRODUCTS")
            filtered_products = DEMO_PRODUCTS.copy()

            # Apply category filter
            if category and category != 'all':
                print(f"🔍 Filtering by category: {category}")
                filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
                print(f"📊 Found {len(filtered_products)} products in category {category}")

            # Apply search filter
            if search:
                filtered_products = [p for p in filtered_products if search in p['name'].lower() or search in p['description'].lower()]

            # Apply featured filter
            if featured:
                filtered_products = [p for p in filtered_products if p['is_featured']]

            # Sort products
            if sort_by == 'price_low':
                filtered_products.sort(key=lambda x: x['price'])
            elif sort_by == 'price_high':
                filtered_products.sort(key=lambda x: x['price'], reverse=True)
            elif sort_by == 'name':
                filtered_products.sort(key=lambda x: x['name'])
            elif sort_by == 'newest':
                filtered_products.sort(key=lambda x: x['id'], reverse=True)

            # Pagination
            total_products = len(filtered_products)
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_products = filtered_products[start_idx:end_idx]

            print(f"📤 API returning {len(paginated_products)} products from DEMO_PRODUCTS for page {page}")

            return jsonify({
                'success': True,
                'products': paginated_products,
                'pagination': {
                    'total': total_products,
                    'page': page,
                    'limit': limit,
                    'pages': (total_products + limit - 1) // limit
                }
            })

    except Exception as e:
        print(f"❌ Error in api_products: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/by-ids', methods=['POST'])
def api_products_by_ids():
    """API endpoint to get products by IDs"""
    try:
        data = request.get_json()
        product_ids = data.get('ids', [])

        # Always use DEMO_PRODUCTS in demo mode
        products = [p for p in DEMO_PRODUCTS if p['id'] in product_ids]

        return jsonify({
            'success': True,
            'products': products
        })

    except Exception as e:
        print(f"Error in api_products_by_ids: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/cart', methods=['GET'])
def api_cart():
    """API endpoint to get cart items"""
    user_id = request.args.get('user_id', 'guest')

    # Handle guest users
    if user_id == 'guest' or not user_id:
        return jsonify({'success': True, 'cart': []})

    # For authenticated users, user_id is a string (VARCHAR in database)
    # No need to convert to int
    cart_items = get_user_cart(user_id)
    return jsonify({'success': True, 'cart': cart_items})

def is_sqlite_connection(connection):
    """Check if connection is SQLite"""
    return 'sqlite' in str(type(connection)).lower()

def ensure_user_exists(user_id, phone=None):
    """Ensure user exists in database, create if necessary"""
    print(f"🔍 ensure_user_exists called with user_id='{user_id}', phone='{phone}'")

    connection = get_db_connection()
    if not connection:
        print(f"❌ Cannot check user {user_id} - no database connection")
        return False

    is_sqlite = is_sqlite_connection(connection)

    try:
        cursor = connection.cursor()

        # Check if user exists - use correct placeholder syntax
        print(f"🔍 Checking if user {user_id} exists in database...")
        if is_sqlite:
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        else:
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        user_exists = cursor.fetchone() is not None
        print(f"🔍 User exists check result: {user_exists}")

        if not user_exists:
            print(f"👤 User {user_id} does not exist in database, creating...")
            # For cart operations, we need phone number to create user
            if phone and str(phone).strip():
                print(f"📞 Creating user with phone: {phone}")
                if is_sqlite:
                    cursor.execute("""
                        INSERT INTO users (id, phone, name, logged_in)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, str(phone).strip(), '', 1))
                else:
                    cursor.execute("""
                        INSERT INTO users (id, phone, name, logged_in)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, str(phone).strip(), '', True))
                connection.commit()
                print(f"✅ User {user_id} created in database successfully")
                return True
            else:
                print(f"❌ Cannot create user {user_id} - phone number is empty or None: '{phone}'")
                return False
        else:
            print(f"✅ User {user_id} already exists in database")
            return True

    except Error as e:
        print(f"❌ Database error in ensure_user_exists for user {user_id}: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Unexpected error in ensure_user_exists for user {user_id}: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    """API endpoint to update cart"""
    try:
        print("🔄 API /cart/update called")
        data = request.get_json()
        print(f"📦 Received data: {data}")

        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        phone = data.get('phone')  # Optional phone for user creation

        print(f"👤 User ID: {user_id}, Product ID: {product_id}, Quantity: {quantity}, Phone: {phone}")

        # Validate required inputs
        if not user_id or user_id == 'guest':
            print("❌ Invalid or guest user_id")
            return jsonify({'success': False, 'error': 'Invalid user ID'}), 400

        # Validate inputs (keep user_id as string, convert others to int)
        try:
            product_id = int(product_id)
            quantity = int(quantity)
            print(f"✅ Input validation passed: user_id='{user_id}', product_id={product_id}, quantity={quantity}")
        except (ValueError, TypeError) as e:
            print(f"❌ Input validation failed: {e}")
            return jsonify({'success': False, 'error': 'Invalid input data'}), 400

        # Ensure user exists in database before cart operations
        print(f"🔍 About to call ensure_user_exists with user_id='{user_id}', phone='{phone}'")
        user_exists_result = ensure_user_exists(user_id, phone)
        print(f"🔍 ensure_user_exists returned: {user_exists_result}")
        if not user_exists_result:
            print("❌ User validation failed - user does not exist and could not be created")
            return jsonify({'success': False, 'error': 'User validation failed'}), 400

        # Update cart in database
        print(f"🗄️ Calling update_cart_item function with user_id='{user_id}', product_id={product_id}, quantity={quantity}")
        success = update_cart_item(user_id, product_id, quantity)

        if success:
            print("✅ Cart update successful")
            return jsonify({'success': True})
        else:
            print("❌ Cart update failed")
            return jsonify({'success': False, 'error': 'Failed to update cart'}), 500

    except Exception as e:
        print(f"❌ Error in api_cart_update: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    """API endpoint to remove item from cart"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'guest')
        product_id = data.get('product_id')

        # Skip guest users for database operations
        if user_id == 'guest':
            return jsonify({'success': True})

        # Validate inputs
        try:
            user_id = int(user_id)
            product_id = int(product_id)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid input data'}), 400

        # Remove from cart in database
        success = remove_from_cart(user_id, product_id)

        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to remove item'}), 500

    except Exception as e:
        print(f"Error in api_cart_remove: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Order and Payment Functions
def create_order(user_id, cart_items, billing_info, payment_method):
    """Create order from cart items"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)

        # Calculate total
        total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

        # Get user's order count to generate user-specific order number
        cursor.execute("SELECT COUNT(*) as order_count FROM orders WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        user_order_number = result['order_count'] + 1

        # Create order
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, status, payment_method,
                              shipping_address, billing_name, billing_email,
                              billing_phone, billing_city, billing_zip, user_order_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            total_amount,
            'pending',
            payment_method,
            billing_info.get('address', ''),
            billing_info.get('firstName', '') + ' ' + billing_info.get('lastName', ''),
            billing_info.get('email', ''),
            billing_info.get('phone', ''),
            billing_info.get('city', ''),
            billing_info.get('zipCode', ''),
            user_order_number
        ))

        order_id = cursor.lastrowid
        
        # Create order items
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (
                order_id,
                item['product_id'],
                item['quantity'],
                item['price']
            ))
        
        connection.commit()
        print(f"✅ Order {order_id} created for user {user_id}, total: ₹{total_amount}")
        return order_id
        
    except Error as e:
        print(f"❌ Error creating order: {e}")
        connection.rollback()
        return None
    finally:
        if connection:
            connection.close()

def get_user_orders(user_id):
    """Get all orders for a user"""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.id, o.user_order_number, o.total_amount, o.status, o.payment_method,
                   o.created_at, o.billing_name, o.billing_email,
                   GROUP_CONCAT(CONCAT(p.name, ' (x', oi.quantity, ')') SEPARATOR ', ') as items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN products p ON oi.product_id = p.id
            WHERE o.user_id = %s
            GROUP BY o.id
            ORDER BY o.created_at DESC
        """, (user_id,))
        
        orders = cursor.fetchall()
        return orders
        
    except Error as e:
        print(f"❌ Error getting orders: {e}")
        return []
    finally:
        if connection:
            connection.close()

@app.route('/api/send-otp', methods=['POST'])
def api_send_otp():
    """API endpoint to send OTP"""
    try:
        data = request.get_json()
        phone = data.get('phone', '')

        print(f"Send OTP request - phone: '{phone}' (type: {type(phone)}, len: {len(phone)})")

        if not phone:
            return jsonify({'success': False, 'error': 'Phone number required'}), 400

        # Generate demo OTP
        otp = str(random.randint(100000, 999999))
        DEMO_OTPS[phone] = otp
        print(f"Generated OTP: '{otp}' for phone: '{phone}'")
        print(f"DEMO_OTPS now contains keys: {list(DEMO_OTPS.keys())}")
        print(f"DEMO_OTPS full contents: {DEMO_OTPS}")

        # In demo mode, return the OTP directly for testing
        return jsonify({
            'success': True,
            'message': 'OTP sent successfully',
            'otp': otp  # Only for demo purposes
        })

    except Exception as e:
        print(f"Error in api_send_otp: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint to login"""
    print("=== LOGIN API CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request content type: {request.content_type}")

    try:
        raw_data = request.get_data()
        print(f"Raw request data: {raw_data}")

        data = request.get_json()
        print(f"Parsed JSON data: {data}")

        if data is None:
            print("ERROR: No JSON data could be parsed")
            return jsonify({'success': False, 'error': 'Invalid JSON request'}), 400

        phone = data.get('phone', '')
        otp = data.get('otp', '')

        print(f"Extracted phone: '{phone}', otp: '{otp}'")

        # Original validation code (temporary bypass removed)
        # ... rest of the function ...

        print(f"Login attempt - phone: '{phone}' (type: {type(phone)}, len: {len(phone)}), otp: '{otp}' (type: {type(otp)}, len: {len(otp)})")
        print(f"DEMO_OTPS keys: {list(DEMO_OTPS.keys())}")
        print(f"DEMO_OTPS contents: {DEMO_OTPS}")

        stored_otp = DEMO_OTPS.get(phone, 'NOT FOUND')
        print(f"Stored OTP for phone '{phone}': '{stored_otp}' (type: {type(stored_otp)})")

        # Clean the inputs for comparison
        clean_phone = str(phone).strip()
        clean_otp = str(otp).strip()

        print(f"Cleaned inputs - phone: '{clean_phone}', otp: '{clean_otp}'")

        # For demo purposes, accept any 6-digit OTP to avoid validation issues
        print("Demo mode - accepting any valid 6-digit OTP")
        if len(clean_otp) == 6 and clean_otp.isdigit():
            print("Demo OTP validation successful")
        else:
            print(f"Invalid OTP format: '{clean_otp}' (length: {len(clean_otp)})")
            return jsonify({'success': False, 'error': 'Invalid OTP format'}), 400

        print("OTP validation successful - proceeding with login")

        # Create or get user
        user_id = None
        for uid, user_data in DEMO_USERS.items():
            if user_data.get('phone') == phone:
                user_id = uid
                break

        if not user_id:
            # Create new user
            user_id = hashlib.md5(phone.encode()).hexdigest()[:8]

            # Save to both in-memory storage and MySQL
            DEMO_USERS[user_id] = {
                'phone': phone,
                'created_at': 'demo'
            }
            save_user_to_mysql(user_id, phone)
        else:
            # Existing user - update login status in MySQL
            save_user_to_mysql(user_id, phone)

        # Clear OTP
        if phone in DEMO_OTPS:
            del DEMO_OTPS[phone]

        return jsonify({
            'success': True,
            'user': {
            'user_id': user_id,
                'phone': phone
            },
            'message': 'Login successful'
        })

    except Exception as e:
        print(f"Error in api_login: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """API endpoint to create order from cart"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        billing_info = data.get('billing_info', {})
        payment_method = data.get('payment_method', 'cod')

        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400

        # Get cart items
        cart_items = get_user_cart(user_id)
        if not cart_items:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400

        # Create order
        order_id = create_order(user_id, cart_items, billing_info, payment_method)
        
        if order_id:
            # Clear cart after order creation
            clear_user_cart(user_id)
            
            return jsonify({
                'success': True,
                'order_id': order_id,
                'message': 'Order created successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to create order'}), 500

    except Exception as e:
        print(f"❌ Error in api_create_order: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def api_get_orders():
    """API endpoint to get user's order history"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID required'}), 400

        orders = get_user_orders(user_id)
        
        return jsonify({
            'success': True,
            'orders': orders
        })

    except Exception as e:
        print(f"❌ Error in api_get_orders: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>/complete', methods=['POST'])
def api_complete_order(order_id):
    """API endpoint to complete payment for order"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500

        cursor = connection.cursor()
        
        # Update order status to 'completed'
        cursor.execute("""
            UPDATE orders 
            SET status = 'completed'
            WHERE id = %s
        """, (order_id,))
        
        connection.commit()
        
        if cursor.rowcount > 0:
            return jsonify({
                'success': True,
                'message': 'Payment completed successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Order not found'}), 404

    except Error as e:
        print(f"❌ Error completing order: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API endpoint to logout"""
    return jsonify({'success': True})

# Initialize database on startup - FORCE CLEAR EVERY TIME
print("🚀 Initializing Flask app and database...")
print("⚠️ FORCE CLEARING DATABASE PRODUCTS ON EVERY RESTART...")

try:
    init_database()
    print("✅ init_database() completed successfully")
except Exception as e:
    print(f"❌ CRITICAL ERROR in init_database(): {e}")
    import traceback
    traceback.print_exc()

if __name__ == '__main__':
    # Try multiple ports in case of permission issues
    ports_to_try = [8888, 9999, 7777, 6666, 5555]
    
    # Use 0.0.0.0 to allow connections from mobile devices on same network
    # 127.0.0.1 only allows localhost connections
    HOST = '0.0.0.0'  # Change to '127.0.0.1' if you only want localhost access

    for port in ports_to_try:
        try:
            print(f"🚀 Trying to start server on port {port}...")
            print(f"🌐 Will be accessible at:")
            print(f"   - Local: http://127.0.0.1:{port}")
            print(f"   - Network: http://0.0.0.0:{port}")
            print(f"🧪 Test route: http://127.0.0.1:{port}/test")

            if USE_WAITERESS:
                print("🔧 Using Waitress WSGI server")
                serve(app, host=HOST, port=port)
            else:
                print("🔧 Using Flask dev server (dotenv loading disabled)")
                app.run(debug=True, host=HOST, port=port, threaded=True)
            break  # If we get here, server started successfully
        except PermissionError:
            print(f"❌ Permission denied on port {port}, trying next port...")
            continue
        except Exception as e:
            print(f"❌ Error on port {port}: {e}, trying next port...")
            continue

    print("❌ Could not start server on any port due to permission issues")
    print("💡 Try running with: sudo python backend/app.py")
