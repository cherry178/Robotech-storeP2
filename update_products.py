#!/usr/bin/env python3

import re

# New DEMO_PRODUCTS with all the products provided by the user
new_products = '''DEMO_PRODUCTS = [
    # Microcontrollers (11 items)
    {
        "id": 1,
        "name": "Adafruit Feather M0",
        "description": "ARM Cortex-M0+ microcontroller board with Bluetooth",
        "price": 650.0,
        "category": "Microcontrollers",
        "stock_quantity": 25,
        "image_url": "https://m.media-amazon.com/images/I/51+N-57gSiL.jpg",
        "is_featured": True
    },
    {
        "id": 2,
        "name": "Arduino Due",
        "description": "ARM Cortex-M3 microcontroller board with 32-bit architecture",
        "price": 2200.0,
        "category": "Microcontrollers",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/736x/d1/66/1b/d1661bdecf277684181694a4fedbf9bf.jpg",
        "is_featured": True
    },
    {
        "id": 3,
        "name": "Arduino Mega",
        "description": "ATmega2560 microcontroller board with expanded I/O",
        "price": 1800.0,
        "category": "Microcontrollers",
        "stock_quantity": 20,
        "image_url": "https://i.pinimg.com/1200x/a1/50/a6/a150a6b5db3d525533522fbba78d999b.jpg",
        "is_featured": True
    },
    {
        "id": 4,
        "name": "Arduino Nano",
        "description": "Compact ATmega328 microcontroller board",
        "price": 250.0,
        "category": "Microcontrollers",
        "stock_quantity": 50,
        "image_url": "https://i.pinimg.com/1200x/5b/09/06/5b09066c572846471a3df3242abd4375.jpg",
        "is_featured": False
    },
    {
        "id": 5,
        "name": "Arduino Uno R3",
        "description": "ATmega328P microcontroller board with USB interface",
        "price": 450.0,
        "category": "Microcontrollers",
        "stock_quantity": 30,
        "image_url": "https://m.media-amazon.com/images/I/51+N-57gSiL.jpg",
        "is_featured": False
    },
    {
        "id": 6,
        "name": "Banana Pi",
        "description": "Single-board computer with Allwinner A20 processor",
        "price": 2500.0,
        "category": "Microcontrollers",
        "stock_quantity": 12,
        "image_url": "https://i.pinimg.com/1200x/c6/da/02/c6da024f4702e68756c6d466894a027c.jpg",
        "is_featured": True
    },
    {
        "id": 7,
        "name": "ESP32 Development Board",
        "description": "WiFi & Bluetooth enabled microcontroller",
        "price": 350.0,
        "category": "Microcontrollers",
        "stock_quantity": 40,
        "image_url": "https://m.media-amazon.com/images/I/21xfvGFiirL.jpg",
        "is_featured": False
    },
    {
        "id": 8,
        "name": "ESP8266",
        "description": "WiFi enabled microcontroller module",
        "price": 150.0,
        "category": "Microcontrollers",
        "stock_quantity": 60,
        "image_url": "https://m.media-amazon.com/images/I/41cBDjOi6eL.jpg",
        "is_featured": False
    },
    {
        "id": 9,
        "name": "Orange Pi",
        "description": "Single-board computer with H3 processor",
        "price": 1800.0,
        "category": "Microcontrollers",
        "stock_quantity": 18,
        "image_url": "https://i.pinimg.com/736x/55/fd/a1/55fda180c7904f25067c840a8302d0a7.jpg",
        "is_featured": True
    },
    {
        "id": 10,
        "name": "Raspberry Pi Zero W",
        "description": "Compact single-board computer with WiFi and Bluetooth",
        "price": 1200.0,
        "category": "Microcontrollers",
        "stock_quantity": 35,
        "image_url": "https://i.pinimg.com/1200x/e4/d6/fa/e4d6fa1f834a4c26203690590de22ea4.jpg",
        "is_featured": False
    },
    {
        "id": 11,
        "name": "Teensy 4.1",
        "description": "ARM Cortex-M7 microcontroller development board",
        "price": 850.0,
        "category": "Microcontrollers",
        "stock_quantity": 22,
        "image_url": "https://i.pinimg.com/1200x/50/5d/4a/505d4ab5dff8115c1dc1e2391ed6d1fb.jpg",
        "is_featured": False
    },

    # Actuators (9 items)
    {
        "id": 12,
        "name": "5V Relay Module",
        "description": "Electromagnetic relay module for switching applications",
        "price": 35.0,
        "category": "Actuators",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/736x/31/a0/60/31a060caefe320fdf1108f364e681f1d.jpg",
        "is_featured": False
    },
    {
        "id": 13,
        "name": "Bluetooth Controlled Linear Actuator",
        "description": "Wireless controlled linear motion actuator",
        "price": 2500.0,
        "category": "Actuators",
        "stock_quantity": 8,
        "image_url": "https://i.pinimg.com/1200x/f7/ba/f5/f7baf50e5993ccffc68e5387bda0b342.jpg",
        "is_featured": True
    },
    {
        "id": 14,
        "name": "Brushless DC Motor",
        "description": "High-efficiency brushless DC motor for precision applications",
        "price": 850.0,
        "category": "Actuators",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/736x/0f/b0/b1/0fb0b100bb886ac9f050213bef229042.jpg",
        "is_featured": False
    },
    {
        "id": 15,
        "name": "Continuous Rotation Robot Servo",
        "description": "360-degree continuous rotation servo motor",
        "price": 180.0,
        "category": "Actuators",
        "stock_quantity": 45,
        "image_url": "https://i.pinimg.com/1200x/51/d7/f8/51d7f86c3ba3a7e9081902780d10d159.jpg",
        "is_featured": False
    },
    {
        "id": 16,
        "name": "DC Motor",
        "description": "12V DC geared motor for robotics and automation projects",
        "price": 150.0,
        "category": "Actuators",
        "stock_quantity": 85,
        "image_url": "https://i.pinimg.com/1200x/d6/ca/b6/d6cab6537f5899be3171be162f5b9fab.jpg",
        "is_featured": False
    },
    {
        "id": 17,
        "name": "H-Bridge DC Stepper Motor Control Module",
        "description": "Dual H-bridge motor driver for stepper motors",
        "price": 120.0,
        "category": "Actuators",
        "stock_quantity": 30,
        "image_url": "https://i.pinimg.com/1200x/f9/f8/fb/f9f8fb91419f05a2436d0a3ca731586a.jpg",
        "is_featured": False
    },
    {
        "id": 18,
        "name": "Motor Driver Shield",
        "description": "Arduino shield for motor control applications",
        "price": 350.0,
        "category": "Actuators",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/4c/45/0f/4c450f39f070b12698645d02dcf10a3a.jpg",
        "is_featured": False
    },
    {
        "id": 19,
        "name": "SG90 Servo Motor",
        "description": "9g micro servo motor for robotics",
        "price": 95.0,
        "category": "Actuators",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/736x/da/53/f7/da53f7c21e5a4b9df6d544bacc1ff085.jpg",
        "is_featured": False
    },
    {
        "id": 20,
        "name": "Stepper Motor",
        "description": "NEMA 17 stepper motor with 1.8° step angle for precision control",
        "price": 450.0,
        "category": "Actuators",
        "stock_quantity": 45,
        "image_url": "https://i.pinimg.com/736x/f1/ba/b4/f1bab45eff6c23f981b993006bd5fcd4.jpg",
        "is_featured": True
    },

    # Sensors (15 items)
    {
        "id": 21,
        "name": "Color Sensor (TCS34725)",
        "description": "RGB color sensor with IR blocking filter",
        "price": 180.0,
        "category": "Sensors",
        "stock_quantity": 40,
        "image_url": "https://i.pinimg.com/1200x/c6/2e/fe/c62efe7156acb4a732ee2a0985cdb1b0.jpg",
        "is_featured": False
    },
    {
        "id": 22,
        "name": "DHT11 Temperature & Humidity Sensor",
        "description": "Digital temperature and humidity sensor with 1-wire interface",
        "price": 45.0,
        "category": "Sensors",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/ef/20/2c/ef202c20c5b52e44bb7cef23d80d31ac.jpg",
        "is_featured": False
    },
    {
        "id": 23,
        "name": "Gas Sensor (MQ-135)",
        "description": "Air quality sensor for detecting harmful gases",
        "price": 90.0,
        "category": "Sensors",
        "stock_quantity": 55,
        "image_url": "https://i.pinimg.com/1200x/fc/51/ee/fc51ee3784738477942608abcf9c8d21.jpg",
        "is_featured": False
    },
    {
        "id": 24,
        "name": "Gas Sensor (MQ-2)",
        "description": "Combustible gas and smoke sensor",
        "price": 85.0,
        "category": "Sensors",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/c0/e7/85/c0e785c8bcfadf88efbdd9bbfbb44e1f.jpg",
        "is_featured": False
    },
    {
        "id": 25,
        "name": "HC-SR04 Ultrasonic Sensor",
        "description": "Ultrasonic ranging sensor for distance measurement",
        "price": 85.0,
        "category": "Sensors",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/1200x/51/f6/84/51f684e16602b2affc0016f1b32bbb0e.jpg",
        "is_featured": False
    },
    {
        "id": 26,
        "name": "Infrared Obstacle Sensor",
        "description": "IR proximity sensor for obstacle detection",
        "price": 35.0,
        "category": "Sensors",
        "stock_quantity": 90,
        "image_url": "https://i.pinimg.com/1200x/22/e1/12/22e1128c1ffb2110402cfa8c977b5f86.jpg",
        "is_featured": False
    },
    {
        "id": 27,
        "name": "Light Sensor (LDR)",
        "description": "Light dependent resistor for light intensity measurement",
        "price": 15.0,
        "category": "Sensors",
        "stock_quantity": 150,
        "image_url": "https://i.pinimg.com/1200x/06/56/d3/0656d3389dc7698d1225cd85dfa5c1e4.jpg",
        "is_featured": False
    },
    {
        "id": 28,
        "name": "PIR Motion Sensor",
        "description": "Passive infrared motion detector sensor",
        "price": 75.0,
        "category": "Sensors",
        "stock_quantity": 65,
        "image_url": "https://i.pinimg.com/1200x/f5/ea/8a/f5ea8a6ffb2e2937f01395b7dadb5394.jpg",
        "is_featured": False
    },
    {
        "id": 29,
        "name": "Pressure Sensor (BMP280)",
        "description": "Barometric pressure and temperature sensor",
        "price": 120.0,
        "category": "Sensors",
        "stock_quantity": 45,
        "image_url": "https://i.pinimg.com/736x/f1/ba/b4/f1bab45eff6c23f981b993006bd5fcd4.jpg",
        "is_featured": False
    },
    {
        "id": 30,
        "name": "Rain Sensor",
        "description": "Rain detection sensor module",
        "price": 75.0,
        "category": "Sensors",
        "stock_quantity": 55,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 31,
        "name": "Sound Sensor",
        "description": "Microphone sound detection module",
        "price": 45.0,
        "category": "Sensors",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },
    {
        "id": 32,
        "name": "Sound Vibration Sensor",
        "description": "Vibration and sound detection sensor",
        "price": 55.0,
        "category": "Sensors",
        "stock_quantity": 70,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },
    {
        "id": 33,
        "name": "Temperature Sensor (DS18B20)",
        "description": "Digital temperature sensor with 1-wire interface",
        "price": 55.0,
        "category": "Sensors",
        "stock_quantity": 85,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },
    {
        "id": 34,
        "name": "Touch Sensor",
        "description": "Capacitive touch sensor module",
        "price": 30.0,
        "category": "Sensors",
        "stock_quantity": 95,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },
    {
        "id": 35,
        "name": "Water Level Sensor",
        "description": "Liquid level detection sensor",
        "price": 65.0,
        "category": "Sensors",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },

    # Displays (7 items)
    {
        "id": 36,
        "name": "7-Segment Display",
        "description": "4-digit 7-segment display with decimal points",
        "price": 65.0,
        "category": "Displays",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/736x/31/a0/60/31a060caefe320fdf1108f364e681f1d.jpg",
        "is_featured": False
    },
    {
        "id": 37,
        "name": "E-paper Display",
        "description": "1.54 inch e-paper display for low power applications",
        "price": 650.0,
        "category": "Displays",
        "stock_quantity": 30,
        "image_url": "https://i.pinimg.com/1200x/50/5d/4a/505d4ab5dff8115c1dc1e2391ed6d1fb.jpg",
        "is_featured": False
    },
    {
        "id": 38,
        "name": "LCD Crystal Display",
        "description": "16x2 character LCD display module with backlight",
        "price": 120.0,
        "category": "Displays",
        "stock_quantity": 85,
        "image_url": "https://i.pinimg.com/736x/55/fd/a1/55fda180c7904f25067c840a8302d0a7.jpg",
        "is_featured": False
    },
    {
        "id": 39,
        "name": "LCD Touchscreen Module",
        "description": "2.4 inch LCD touchscreen module for user interfaces",
        "price": 1200.0,
        "category": "Displays",
        "stock_quantity": 15,
        "image_url": "https://i.pinimg.com/1200x/f7/ba/f5/f7baf50e5993ccffc68e5387bda0b342.jpg",
        "is_featured": True
    },
    {
        "id": 40,
        "name": "LED Matrix Display",
        "description": "8x8 LED matrix display with MAX7219 driver",
        "price": 95.0,
        "category": "Displays",
        "stock_quantity": 70,
        "image_url": "https://i.pinimg.com/736x/0f/b0/b1/0fb0b100bb886ac9f050213bef229042.jpg",
        "is_featured": False
    },
    {
        "id": 41,
        "name": "OLED Display",
        "description": "0.96 inch I2C OLED display module with 128x64 resolution",
        "price": 150.0,
        "category": "Displays",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/fd/ef/d4/fdefd4f32f98c1a2c6f15b71c12ecc75.jpg",
        "is_featured": False
    },
    {
        "id": 42,
        "name": "TFT Screen",
        "description": "2.8 inch TFT LCD color touch screen display",
        "price": 850.0,
        "category": "Displays",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/e4/d6/fa/e4d6fa1f834a4c26203690590de22ea4.jpg",
        "is_featured": True
    },

    # Power Supply (6 items)
    {
        "id": 43,
        "name": "2 Battery Holders",
        "description": "AA battery holder for 2 batteries in series",
        "price": 25.0,
        "category": "Power Supply",
        "stock_quantity": 150,
        "image_url": "https://i.pinimg.com/1200x/51/d7/f8/51d7f86c3ba3a7e9081902780d10d159.jpg",
        "is_featured": False
    },
    {
        "id": 44,
        "name": "3 Battery Holders",
        "description": "AA battery holder for 3 batteries in series",
        "price": 35.0,
        "category": "Power Supply",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/d6/ca/b6/d6cab6537f5899be3171be162f5b9fab.jpg",
        "is_featured": False
    },
    {
        "id": 45,
        "name": "DC-DC Converter",
        "description": "Adjustable DC-DC buck converter module 5V-35V",
        "price": 85.0,
        "category": "Power Supply",
        "stock_quantity": 90,
        "image_url": "https://i.pinimg.com/1200x/f9/f8/fb/f9f8fb91419f05a2436d0a3ca731586a.jpg",
        "is_featured": False
    },
    {
        "id": 46,
        "name": "Linear Voltage Regulator",
        "description": "LM7805 5V linear voltage regulator IC",
        "price": 15.0,
        "category": "Power Supply",
        "stock_quantity": 300,
        "image_url": "https://i.pinimg.com/736x/f1/ba/b4/f1bab45eff6c23f981b993006bd5fcd4.jpg",
        "is_featured": False
    },
    {
        "id": 47,
        "name": "Lithium Polymer Battery",
        "description": "3.7V 1000mAh LiPo battery with JST connector",
        "price": 250.0,
        "category": "Power Supply",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/736x/da/53/f7/da53f7c21e5a4b9df6d544bacc1ff085.jpg",
        "is_featured": False
    },
    {
        "id": 48,
        "name": "Power Bank Module",
        "description": "18650 lithium battery power bank module",
        "price": 180.0,
        "category": "Power Supply",
        "stock_quantity": 60,
        "image_url": "https://i.pinimg.com/1200x/4c/45/0f/4c450f39f070b12698645d02dcf10a3a.jpg",
        "is_featured": False
    },

    # Tools & Accessories (6 items)
    {
        "id": 49,
        "name": "Breadboard",
        "description": "830 tie-point solderless breadboard for prototyping",
        "price": 85.0,
        "category": "Tools & Accessories",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/c6/2e/fe/c62efe7156acb4a732ee2a0985cdb1b0.jpg",
        "is_featured": False
    },
    {
        "id": 50,
        "name": "Male-Female Jumper Wires",
        "description": "40-piece male-to-female jumper wire set",
        "price": 50.0,
        "category": "Tools & Accessories",
        "stock_quantity": 180,
        "image_url": "https://i.pinimg.com/1200x/fc/51/ee/fc51ee3784738477942608abcf9c8d21.jpg",
        "is_featured": False
    },
    {
        "id": 51,
        "name": "Male-Male Jumper Wires",
        "description": "40-piece male-to-male jumper wire set",
        "price": 45.0,
        "category": "Tools & Accessories",
        "stock_quantity": 200,
        "image_url": "https://i.pinimg.com/1200x/ef/20/2c/ef202c20c5b52e44bb7cef23d80d31ac.jpg",
        "is_featured": False
    },
    {
        "id": 52,
        "name": "Nuts & Bolts Kit",
        "description": "Assorted nuts and bolts set for electronics projects",
        "price": 65.0,
        "category": "Tools & Accessories",
        "stock_quantity": 80,
        "image_url": "https://i.pinimg.com/1200x/51/f6/84/51f684e16602b2affc0016f1b32bbb0e.jpg",
        "is_featured": False
    },
    {
        "id": 53,
        "name": "PCB Prototyping Board",
        "description": "Double-sided PCB prototyping board with copper pads",
        "price": 120.0,
        "category": "Tools & Accessories",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/c0/e7/85/c0e785c8bcfadf88efbdd9bbfbb44e1f.jpg",
        "is_featured": False
    },
    {
        "id": 54,
        "name": "USB Cable",
        "description": "USB 2.0 A to B cable for programming and data transfer",
        "price": 35.0,
        "category": "Tools & Accessories",
        "stock_quantity": 250,
        "image_url": "https://i.pinimg.com/736x/96/2a/9d/962a9d51a7b74ec70de4609d1f255f00.jpg",
        "is_featured": False
    },

    # Audio Components (6 items)
    {
        "id": 55,
        "name": "Active Buzzer Module",
        "description": "Electronic buzzer module with built-in oscillator",
        "price": 25.0,
        "category": "Audio Components",
        "stock_quantity": 100,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 56,
        "name": "Audio Adapter Board",
        "description": "Audio amplifier board with speaker connector",
        "price": 120.0,
        "category": "Audio Components",
        "stock_quantity": 50,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 57,
        "name": "Electret Microphone Module",
        "description": "Condenser microphone module for audio input",
        "price": 40.0,
        "category": "Audio Components",
        "stock_quantity": 75,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 58,
        "name": "Passive Buzzer",
        "description": "Piezo buzzer for audio output without oscillator",
        "price": 20.0,
        "category": "Audio Components",
        "stock_quantity": 120,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    },
    {
        "id": 59,
        "name": "Robocraze Speech Recognition Module",
        "description": "Voice command recognition module",
        "price": 450.0,
        "category": "Audio Components",
        "stock_quantity": 20,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": True
    },
    {
        "id": 60,
        "name": "Voice Recognition Microphone Board",
        "description": "Advanced voice recognition and processing board",
        "price": 350.0,
        "category": "Audio Components",
        "stock_quantity": 25,
        "image_url": "https://i.pinimg.com/1200x/f5/25/29/f525292fb2911c4456c36024197caa1a.jpg",
        "is_featured": False
    }
]'''

def update_products():
    # Read the backend file
    with open('backend/app.py', 'r') as f:
        content = f.read()

    # Find and replace the DEMO_PRODUCTS section
    # Look for the pattern from "DEMO_PRODUCTS = [" to the closing "]"
    start_pattern = r'DEMO_PRODUCTS\s*=\s*\['
    end_pattern = r'\]'

    start_match = re.search(start_pattern, content)
    if not start_match:
        print("Could not find DEMO_PRODUCTS start")
        return False

    start_pos = start_match.start()

    # Find the matching closing bracket
    bracket_count = 0
    end_pos = start_pos
    for i in range(start_pos, len(content)):
        if content[i] == '[':
            bracket_count += 1
        elif content[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                end_pos = i + 1
                break

    if bracket_count != 0:
        print("Could not find matching closing bracket")
        return False

    # Replace the DEMO_PRODUCTS section
    before = content[:start_pos]
    after = content[end_pos:]

    new_content = before + new_products + after

    # Write back to file
    with open('backend/app.py', 'w') as f:
        f.write(new_content)

    print("✅ Successfully updated DEMO_PRODUCTS in backend/app.py")
    print("📦 Added 60 products across 8 categories")
    return True

if __name__ == '__main__':
    update_products()
