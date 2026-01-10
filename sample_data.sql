-- Sample data for Robotech Store

USE robotech_store;

-- Insert categories
INSERT INTO categories (name, description) VALUES
('Sensors', 'Various sensors for IoT applications'),
('Microcontrollers', 'Arduino, Raspberry Pi, ESP boards'),
('Actuators', 'Motors, servos, relays'),
('Communication', 'WiFi, Bluetooth, GSM modules'),
('Power Supply', 'Batteries, regulators, converters'),
('Displays', 'LCD, OLED, LED displays'),
('Tools & Accessories', 'Development tools and accessories');

-- Insert sample products
INSERT INTO products (name, description, price, category, subcategory, stock_quantity, specifications, is_featured) VALUES
-- Sensors
('DHT11 Temperature & Humidity Sensor', 'Digital temperature and humidity sensor with 1-wire interface', 45.00, 'Sensors', 'Environmental', 100, '{"accuracy": "±2°C, ±5%RH", "voltage": "3.3-5V", "interface": "Digital"}', true),
('HC-SR04 Ultrasonic Sensor', 'Ultrasonic ranging sensor for distance measurement', 85.00, 'Sensors', 'Distance', 75, '{"range": "2-400cm", "accuracy": "3mm", "voltage": "5V"}', true),
('MPU-6050 IMU Sensor', '6-axis motion tracking device with accelerometer and gyroscope', 120.00, 'Sensors', 'Motion', 50, '{"axes": "6", "interface": "I2C", "voltage": "3.3-5V"}', false),
('PIR Motion Sensor', 'Passive infrared motion detector', 65.00, 'Sensors', 'Motion', 80, '{"detection_range": "3-7m", "angle": "120°", "voltage": "5-12V"}', false),

-- Microcontrollers
('Arduino Uno R3', 'ATmega328P microcontroller board with USB interface', 450.00, 'Microcontrollers', 'Arduino', 30, '{"processor": "ATmega328P", "clock": "16MHz", "voltage": "5V"}', true),
('ESP32 Development Board', 'WiFi & Bluetooth enabled microcontroller', 350.00, 'Microcontrollers', 'ESP', 40, '{"wifi": "2.4GHz", "bluetooth": "4.2", "cores": "2"}', true),
('Raspberry Pi 4 Model B', 'Single-board computer with 4GB RAM', 2800.00, 'Microcontrollers', 'Raspberry Pi', 15, '{"ram": "4GB", "processor": "1.5GHz quad-core", "wifi": "2.4/5GHz"}', true),
('NodeMCU ESP8266', 'WiFi enabled development board', 250.00, 'Microcontrollers', 'ESP', 60, '{"wifi": "2.4GHz", "flash": "4MB", "voltage": "3.3V"}', false),

-- Actuators
('SG90 Servo Motor', '9g micro servo motor for robotics', 95.00, 'Actuators', 'Servos', 120, '{"torque": "1.8kg/cm", "speed": "0.1s/60°", "voltage": "4.8-6V"}', true),
('DC Gear Motor', '12V DC motor with gearbox for robotics', 180.00, 'Actuators', 'Motors', 45, '{"voltage": "12V", "rpm": "100", "torque": "2kg/cm"}', false),
('5V Relay Module', 'Single channel relay module for switching applications', 75.00, 'Actuators', 'Relays', 90, '{"channels": "1", "voltage": "5V", "current": "10A"}', false),

-- Communication
('HC-05 Bluetooth Module', 'Serial Bluetooth transceiver module', 220.00, 'Communication', 'Bluetooth', 35, '{"range": "10m", "interface": "UART", "voltage": "3.6-6V"}', false),
('ESP8266 WiFi Module', 'Serial WiFi transceiver module', 180.00, 'Communication', 'WiFi', 40, '{"standard": "802.11b/g/n", "interface": "UART", "voltage": "3.3V"}', false),
('SIM800L GSM Module', 'Quad-band GSM/GPRS module', 450.00, 'Communication', 'GSM', 25, '{"bands": "850/900/1800/1900MHz", "interface": "UART", "voltage": "3.7-4.2V"}', false),

-- Power Supply
('LM2596 DC-DC Buck Converter', 'Step-down voltage regulator module', 85.00, 'Power Supply', 'Converters', 70, '{"input": "4.5-40V", "output": "1.5-35V", "current": "3A"}', false),
('18650 Battery Holder', 'Single cell lithium battery holder with protection', 45.00, 'Power Supply', 'Batteries', 150, '{"cells": "1", "protection": "Overcharge/Discharge", "current": "1A"}', false),
('5V Power Supply Module', 'AC-DC power supply module', 120.00, 'Power Supply', 'AC-DC', 55, '{"input": "110-220VAC", "output": "5V", "current": "2A"}', false),

-- Displays
('16x2 LCD Display', 'Character LCD display with I2C interface', 150.00, 'Displays', 'LCD', 65, '{"size": "16x2", "interface": "I2C", "backlight": "Blue"}', true),
('0.96" OLED Display', '128x64 OLED display module', 200.00, 'Displays', 'OLED', 45, '{"resolution": "128x64", "interface": "I2C", "diagonal": "0.96\\""}', true),
('7-Segment Display', '4-digit 7-segment display module', 85.00, 'Displays', '7-Segment', 80, '{"digits": "4", "color": "Red", "interface": "Digital"}', false),

-- Tools & Accessories
('Jumper Wires Set', 'Male to male jumper wires (40pcs)', 65.00, 'Tools & Accessories', 'Wires', 200, '{"count": "40", "length": "20cm", "type": "Male-Male"}', false),
('Breadboard 400 Points', 'Solderless breadboard for prototyping', 95.00, 'Tools & Accessories', 'Breadboards', 85, '{"points": "400", "size": "5.5x8.5cm", "binding_posts": "4"}', false),
('Arduino Sensor Kit', 'Complete sensor kit for Arduino projects', 850.00, 'Tools & Accessories', 'Kits', 20, '{"sensors": "10+", "modules": "15", "compatibility": "Arduino"}', true);
