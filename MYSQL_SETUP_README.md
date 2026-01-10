# MySQL Database Setup for Robotech Store

This guide will help you migrate from SQLite to MySQL database without changing any frontend code.

## Prerequisites

1. **MySQL Server** installed and running
2. **Python MySQL connector** (already in requirements.txt)
3. **MySQL root user** access

## Step 1: Install MySQL

### Windows:
```bash
# Download and install MySQL from https://dev.mysql.com/downloads/windows/
# Or use XAMPP which includes MySQL
```

### macOS:
```bash
brew install mysql
brew services start mysql
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
```

## Step 2: Setup MySQL Database

1. **Login to MySQL as root:**
```bash
mysql -u root -p
```

2. **Create database:**
```sql
CREATE DATABASE robotech_store;
EXIT;
```

3. **Run the setup script:**
```bash
cd backend
python setup_mysql.py
```

## Step 3: Configure Flask App

1. **Edit `backend/app.py`:**
   - Find the `DB_CONFIG` section
   - Update the password:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_actual_mysql_password',  # Change this
    'database': 'robotech_store'
}
```

## Step 4: Test the Setup

1. **Start the Flask server:**
```bash
python backend/app.py
```

2. **Test the API endpoints:**
   - Visit: `http://localhost:5000/api/products`
   - Should return products from MySQL database

3. **Test cart functionality:**
   - Frontend will work unchanged
   - Cart data now persists in MySQL instead of localStorage

## Database Schema

The MySQL database includes these tables:

- **`users`**: User accounts and authentication
- **`products`**: Product catalog with pricing and images
- **`carts`**: Shopping cart items with user relationships

## Key Changes Made

1. **Replaced in-memory storage** with MySQL database calls
2. **Updated API endpoints** to use database queries instead of DEMO_* dictionaries
3. **Added database connection functions** with error handling
4. **Created setup script** for easy database initialization

## Frontend Compatibility

- **No frontend changes required**
- **All existing API calls work unchanged**
- **Cart functionality identical**
- **User experience unchanged**

## Troubleshooting

### Connection Error:
```
Error connecting to MySQL: Access denied
```
**Solution:** Check MySQL credentials in `DB_CONFIG`

### Database Not Found:
```
Unknown database 'robotech_store'
```
**Solution:** Run `python setup_mysql.py` again

### Permission Error:
```
Access denied for user 'root'@'localhost'
```
**Solution:** Grant permissions in MySQL:
```sql
GRANT ALL PRIVILEGES ON robotech_store.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Migration Complete!

Your Robotech Store now uses **MySQL** for persistent data storage while maintaining full **frontend compatibility**.
