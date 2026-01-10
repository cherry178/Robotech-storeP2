# Robotech Store - Startup Guide

This guide shows you how to start the Robotech Store project easily, even after closing Cursor and the terminal.

## 🚀 Quick Start Options

### Option 1: Desktop App (Recommended for macOS)
1. **Double-click the `RobotechStore.app`** file in your project folder
2. The app will automatically:
   - Check and start MySQL (if needed)
   - Start the Flask backend server
   - Open your browser to the store

### Option 2: Quick Start Script
```bash
./quick_start.sh
```
This runs the comprehensive startup script that handles everything automatically.

### Option 3: Full Control Script
```bash
./start_project.sh
```
This provides detailed output and status information while starting all services.

## 📋 What Happens When You Start

The startup scripts will:

1. **Check MySQL Status**
   - Verify MySQL is running
   - Start MySQL service if needed (macOS/Linux)
   - Show clear error messages if MySQL setup is required

2. **Start Backend Server**
   - Navigate to `backend/` directory
   - Install/update Python dependencies
   - Start Flask server on port 8888
   - Provide backend API at `http://localhost:8888`

3. **Start Frontend Server** (if needed)
   - Check for React/Node.js frontend
   - Start development server on port 3000
   - Or start simple HTTP server on port 7000 for static files

4. **Display Status**
   - Show all running URLs
   - Provide test links
   - Keep services running until you press Ctrl+C

## 🌐 Access Your Store

Once started, access these URLs:

- **Home Page**: http://localhost:8888/
- **Products**: http://localhost:8888/products
- **Cart**: http://localhost:8888/cart
- **Orders**: http://localhost:8888/orders
- **Payment**: http://localhost:8888/payment

## 🛠️ Manual Setup (if needed)

If the automatic scripts don't work, you can start services manually:

### Start MySQL
```bash
# macOS
brew services start mysql

# Ubuntu/Debian
sudo systemctl start mysql

# Windows
# Start MySQL from Windows Services panel
```

### Start Backend
```bash
cd backend
python3 app.py
```

### Start Frontend (if separate)
```bash
# If using React/Node.js
npm start

# Or for simple static files
python3 -m http.server 7000
```

## 📁 Project Structure

```
RobotechStore/
├── backend/           # Flask API server
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── start_project.sh  # Comprehensive startup script
├── quick_start.sh    # Simple startup script
├── RobotechStore.app # macOS desktop app
└── README_STARTUP.md # This file
```

## 🔧 Troubleshooting

### MySQL Connection Issues
- Make sure MySQL is installed
- Check if MySQL service is running
- Verify root user has no password (default setup)

### Port Conflicts
- Scripts automatically kill processes using ports 8888, 7000, 3000
- If issues persist, manually kill processes:
  ```bash
  lsof -ti:8888 | xargs kill -9
  ```

### Permission Issues
- Make sure scripts are executable:
  ```bash
  chmod +x start_project.sh quick_start.sh
  ```

## 💡 Pro Tips

1. **Keep the terminal window open** - Services run in the background but the script monitors them
2. **Use the desktop app** for the easiest experience on macOS
3. **Check the logs** if something goes wrong:
   - Backend logs: `backend.log`
   - Frontend logs: `frontend.log`

## 🎯 What Works Now

- ✅ Automatic MySQL startup
- ✅ Flask backend server (port 8888)
- ✅ Frontend serving (port 7000/3000)
- ✅ Cart functionality
- ✅ User authentication
- ✅ Payment processing
- ✅ Order management
- ✅ Product catalog
- ✅ Responsive design

Your Robotech Store is now ready to run with a single click!
