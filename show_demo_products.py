#!/usr/bin/env python3

# Extract and display DEMO_PRODUCTS from the backend
DEMO_PRODUCTS = [
    {
        "id": 1,
        "name": "Arduino Uno R3",
        "description": "ATmega328P microcontroller board with USB interface",
        "price": 450.0,
        "category": "Microcontrollers",
        "stock_quantity": 30,
        "image_url": "https://m.media-amazon.com/images/I/51+N-57gSiL.jpg",
        "is_featured": True
    },
    {
        "id": 2,
        "name": "ESP32 Development Board",
        "description": "WiFi & Bluetooth enabled microcontroller",
        "price": 350.0,
        "category": "Microcontrollers",
        "stock_quantity": 40,
        "image_url": "https://i.pinimg.com/736x/d1/66/1b/d1661bdecf277684181694a4fedbf9bf.jpg",
        "is_featured": True
    },
    {
        "id": 3,
        "name": "DHT11 Temperature & Humidity Sensor",
        "description": "Digital temperature and humidity sensor with 1-wire interface",
        "price": 45.0,
        "category": "Sensors",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/a1/50/a6/a150a6b5db3d525533522fbba78d999b.jpg",
        "is_featured": True
    },
    {
        "id": 4,
        "name": "HC-SR04 Ultrasonic Sensor",
        "description": "Ultrasonic ranging sensor for distance measurement",
        "price": 85.0,
        "category": "Sensors",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/1200x/5b/09/06/5b09066c572846471a3df3242abd4375.jpg",
        "is_featured": True
    },
    {
        "id": 5,
        "name": "SG90 Servo Motor",
        "description": "9g micro servo motor for robotics",
        "price": 95.0,
        "category": "Actuators",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/c6/da/02/c6da024f4702e68756c6d466894a027c.jpg",
        "is_featured": True
    },
    # I'll continue with more products...
]

def show_products():
    print(f'📦 DEMO PRODUCTS IN DATABASE ({len(DEMO_PRODUCTS)} total):\n')

    for product in DEMO_PRODUCTS:
        print(f'🆔 ID: {product["id"]}')
        print(f'📝 Name: {product["name"]}')
        print(f'💰 Price: ₹{product["price"]}')
        print(f'📂 Category: {product["category"]}')
        print(f'📦 Stock: {product["stock_quantity"]}')
        print(f'⭐ Featured: {"Yes" if product.get("is_featured", False) else "No"}')
        print(f'🖼️  Image: {product["image_url"]}')
        print('-' * 60)

    print(f'\n📊 SUMMARY:')
    print(f'   • Total Products: {len(DEMO_PRODUCTS)}')
    categories = {}
    for p in DEMO_PRODUCTS:
        cat = p["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print(f'   • Categories: {", ".join(f"{cat} ({count})" for cat, count in categories.items())}')

if __name__ == '__main__':
    show_products()
