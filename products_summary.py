#!/usr/bin/env python3

# Complete list of products based on DEMO_PRODUCTS from backend/app.py
products = [
    # Microcontrollers (IDs 1-2)
    {"id": 1, "name": "Arduino Uno R3", "price": 450.0, "category": "Microcontrollers", "featured": True},
    {"id": 2, "name": "ESP32 Development Board", "price": 350.0, "category": "Microcontrollers", "featured": True},

    # Sensors (IDs 3-4)
    {"id": 3, "name": "DHT11 Temperature & Humidity Sensor", "price": 45.0, "category": "Sensors", "featured": True},
    {"id": 4, "name": "HC-SR04 Ultrasonic Sensor", "price": 85.0, "category": "Sensors", "featured": True},

    # Actuators (IDs 5-7)
    {"id": 5, "name": "SG90 Servo Motor", "price": 95.0, "category": "Actuators", "featured": True},
    {"id": 6, "name": "DC Motor", "price": 150.0, "category": "Actuators", "featured": True},
    {"id": 7, "name": "Stepper Motor", "price": 450.0, "category": "Actuators", "featured": True},

    # Displays (IDs 8-14)
    {"id": 8, "name": "LCD Crystal Display", "price": 120.0, "category": "Displays", "featured": False},
    {"id": 9, "name": "OLED Display", "price": 150.0, "category": "Displays", "featured": False},
    {"id": 10, "name": "TFT Screen", "price": 850.0, "category": "Displays", "featured": True},
    {"id": 11, "name": "7-Segment Display", "price": 65.0, "category": "Displays", "featured": False},
    {"id": 12, "name": "E-paper Display", "price": 650.0, "category": "Displays", "featured": False},
    {"id": 13, "name": "LED Matrix Display", "price": 95.0, "category": "Displays", "featured": False},
    {"id": 14, "name": "LCD Touchscreen Module", "price": 1200.0, "category": "Displays", "featured": True},

    # Power Supply (IDs 15-18, 22, 28)
    {"id": 15, "name": "2 Battery Holders", "price": 25.0, "category": "Power Supply", "featured": False},
    {"id": 16, "name": "3 Battery Holders", "price": 35.0, "category": "Power Supply", "featured": False},
    {"id": 17, "name": "DC-DC Converter", "price": 85.0, "category": "Power Supply", "featured": False},
    {"id": 18, "name": "Power Bank Module", "price": 180.0, "category": "Power Supply", "featured": False},
    {"id": 22, "name": "Lithium Polymer Battery", "price": 250.0, "category": "Power Supply", "featured": False},
    {"id": 28, "name": "Linear Voltage Regulator", "price": 15.0, "category": "Power Supply", "featured": False},

    # Tools & Accessories (IDs 19-21, 23-24, 30)
    {"id": 19, "name": "Breadboard", "price": 85.0, "category": "Tools & Accessories", "featured": False},
    {"id": 20, "name": "Male-Male Jumper Wires", "price": 45.0, "category": "Tools & Accessories", "featured": False},
    {"id": 21, "name": "Male-Female Jumper Wires", "price": 50.0, "category": "Tools & Accessories", "featured": False},
    {"id": 23, "name": "PCB Prototyping Board", "price": 120.0, "category": "Tools & Accessories", "featured": False},
    {"id": 24, "name": "Nuts & Bolts Kit", "price": 65.0, "category": "Tools & Accessories", "featured": False},
    {"id": 30, "name": "USB Cable", "price": 35.0, "category": "Tools & Accessories", "featured": False},

    # Robotics (IDs 25-27)
    {"id": 25, "name": "Cooling Fan 5V", "price": 45.0, "category": "Robotics", "featured": False},
    {"id": 26, "name": "Tires", "price": 30.0, "category": "Robotics", "featured": False},
    {"id": 27, "name": "Wheels", "price": 25.0, "category": "Robotics", "featured": False},

    # Audio Components (ID 29)
    {"id": 29, "name": "Audio Adapter Board", "price": 120.0, "category": "Audio Components", "featured": False},
]

def show_products():
    print(f'📦 PRODUCTS IN ROBOTECH STORE DATABASE ({len(products)} total):\n')

    # Group by category
    categories = {}
    featured_count = 0
    total_value = 0

    for product in products:
        cat = product['category']
        categories[cat] = categories.get(cat, []) + [product]
        if product['featured']:
            featured_count += 1
        total_value += product['price']

    print(f'📊 SUMMARY:')
    print(f'   • Total Products: {len(products)}')
    print(f'   • Featured Products: {featured_count}')
    print(f'   • Total Inventory Value: ₹{total_value:,.0f}')
    print(f'   • Categories: {len(categories)}')
    print()

    # Show products by category
    for category, prods in sorted(categories.items()):
        print(f'📂 {category} ({len(prods)} products):')
        for product in sorted(prods, key=lambda x: x['id']):
            featured = "⭐" if product['featured'] else "  "
            print(f'   {featured} #{product["id"]:2d}: {product["name"]} - ₹{product["price"]:,.0f}')
        print()

    print('💡 These products should be loaded into your MySQL database when the backend starts.')
    print('   If cart items aren\'t showing, check if the backend server is running and MySQL is connected.')

if __name__ == '__main__':
    show_products()
