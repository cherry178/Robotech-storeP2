# 🚀 Robotech Store - Quick Start Guide

## ⚡ Start Server in Background (Runs Even After Closing Cursor/Terminal)

### One Command to Start Everything:
```bash
cd /Users/charishmarasineni/Store
./start_background_server.sh
```

**That's it!** The server will run in the background and continue working even after you close Cursor and Terminal.

---

## 📱 Access from Mobile & Laptop

### On Your Laptop:
Open browser and go to: **http://127.0.0.1:8888**

### On Your Mobile Phone:
1. Make sure your phone and computer are on the **same Wi-Fi network**
2. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   (Look for something like `192.168.1.100`)
3. On your phone's browser, open:
   ```
   http://YOUR_IP_ADDRESS:8888
   ```
   Example: `http://192.168.1.100:8888`

---

## 🛠️ Useful Commands

| What You Want | Command |
|---------------|---------|
| **Start server** | `./start_background_server.sh` |
| **Check if running** | `./check_server.sh` |
| **Stop server** | `./stop_server.sh` |
| **View logs** | `tail -f logs/server.log` |
| **View errors** | `tail -f logs/server_error.log` |

---

## ✅ Verify It's Working

1. Run: `./check_server.sh`
2. Open browser: `http://127.0.0.1:8888`
3. You should see the Robotech Store homepage!

---

## 🔧 Troubleshooting

### "Port already in use"
```bash
./stop_server.sh
./start_background_server.sh
```

### "Permission denied"
```bash
chmod +x start_background_server.sh
chmod +x stop_server.sh
chmod +x check_server.sh
```

### Can't access from mobile
- Make sure both devices are on the same Wi-Fi
- Check firewall settings on your computer
- Verify server is running: `./check_server.sh`

---

## 📝 Important Notes

- ✅ Server runs in **background** - continues after closing apps
- ✅ Works on **both mobile and laptop**
- ✅ Logs saved in `logs/` folder
- ✅ To stop: run `./stop_server.sh`

---

## 🎉 You're All Set!

Just run `./start_background_server.sh` and your website will be accessible on both mobile and laptop, even after closing Cursor and Terminal!
