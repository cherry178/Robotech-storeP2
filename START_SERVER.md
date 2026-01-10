# How to Start the Robotech Store Server

## Quick Start (Easiest Method)

### Option 1: Using the Quick Start Script (Recommended)
```bash
cd /Users/charishmarasineni/Store
chmod +x quick_start.sh
./quick_start.sh
```

### Option 2: Using the Start Project Script
```bash
cd /Users/charishmarasineni/Store
chmod +x start_project.sh
./start_project.sh
```

### Option 3: Manual Start (If scripts don't work)
```bash
cd /Users/charishmarasineni/Store

# Install dependencies (if not already installed)
pip3 install -r requirements.txt

# Start the server
cd backend
python3 app.py
```

## After Starting

Once the server starts, you should see:
```
🚀 Trying to start server on port 8888...
🌐 Will be accessible at http://127.0.0.1:8888
```

Then open your browser and go to:
- **http://127.0.0.1:8888/** (Home page)
- **http://127.0.0.1:8888/products** (Products page)
- **http://127.0.0.1:8888/cart** (Cart page)

## For Mobile Testing

1. Make sure your computer and mobile device are on the same Wi-Fi network
2. Find your computer's local IP address:
   - **macOS/Linux**: Run `ifconfig | grep "inet " | grep -v 127.0.0.1`
   - **Windows**: Run `ipconfig` and look for IPv4 Address
3. On your mobile device, open: `http://YOUR_IP_ADDRESS:8888`
   - Example: `http://192.168.1.100:8888`

## Troubleshooting

### Port Already in Use
If you get "port already in use" error:
```bash
# Kill process on port 8888
lsof -ti:8888 | xargs kill -9
```

### Permission Denied
If you get permission errors:
```bash
# Try with sudo (not recommended, but works)
sudo python3 backend/app.py
```

### Dependencies Missing
If you get import errors:
```bash
pip3 install flask flask-cors mysql-connector-python waitress
```

### Server Won't Start
1. Check if Python 3 is installed: `python3 --version`
2. Check if all dependencies are installed: `pip3 list | grep flask`
3. Check the error messages in the terminal

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.
