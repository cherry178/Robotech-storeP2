# Permanent Server Setup Guide

## 🎯 Goal: Run Server in Background (Even After Closing Cursor/Terminal)

## Quick Start (Easiest Method)

### Step 1: Start the Server in Background
```bash
cd /Users/charishmarasineni/Store
./start_background_server.sh
```

That's it! The server will now run in the background and continue even after you close Terminal or Cursor.

### Step 2: Check if Server is Running
```bash
./check_server.sh
```

### Step 3: Stop the Server (When Needed)
```bash
./stop_server.sh
```

## 📱 Accessing from Mobile

1. **Make sure your computer and phone are on the same Wi-Fi network**

2. **Find your computer's IP address:**
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   Look for something like `192.168.1.100` or `10.0.0.50`

3. **On your phone's browser, open:**
   ```
   http://YOUR_IP_ADDRESS:8888
   ```
   Example: `http://192.168.1.100:8888`

## 🖥️ Accessing from Laptop

Simply open in your browser:
```
http://127.0.0.1:8888
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `./start_background_server.sh` | Start server in background |
| `./stop_server.sh` | Stop the server |
| `./check_server.sh` | Check if server is running |
| `tail -f logs/server.log` | View server logs in real-time |
| `tail -f logs/server_error.log` | View error logs |

## 🔧 Troubleshooting

### Server Won't Start
1. Check if port 8888 is already in use:
   ```bash
   lsof -ti:8888
   ```
2. Kill any existing process:
   ```bash
   ./stop_server.sh
   ```
3. Check error logs:
   ```bash
   cat logs/server_error.log
   ```

### Can't Access from Mobile
1. Make sure both devices are on the same Wi-Fi
2. Check your computer's firewall settings
3. Verify the server is running: `./check_server.sh`
4. Try accessing from laptop first: `http://127.0.0.1:8888`

### Server Stops After Closing Terminal
- Make sure you used `./start_background_server.sh` (not just `python3 app.py`)
- The `nohup` command ensures it runs in background
- Check logs to see if there was an error: `cat logs/server_error.log`

## 🚀 Auto-Start on Boot (Optional)

If you want the server to start automatically when your computer boots:

### Method 1: Using launchd (macOS)
```bash
# Copy the plist file to LaunchAgents
cp com.robotechstore.server.plist ~/Library/LaunchAgents/

# Load the service
launchctl load ~/Library/LaunchAgents/com.robotechstore.server.plist

# Start it now
launchctl start com.robotechstore.server
```

### Method 2: Add to Login Items (macOS)
1. System Preferences → Users & Groups → Login Items
2. Add the `start_background_server.sh` script

## 📝 Notes

- The server runs in the background using `nohup`
- Logs are saved in the `logs/` directory
- The server will continue running even after closing all applications
- To stop it, use `./stop_server.sh` or restart your computer

## ✅ Verification

After starting, verify it's working:
1. Check status: `./check_server.sh`
2. Open browser: `http://127.0.0.1:8888`
3. Check logs: `tail -f logs/server.log`

If all three work, you're good to go! 🎉
