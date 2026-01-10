# 🛍️ Robotech Store

A full-featured e-commerce store for robotics components with user authentication, shopping cart, payment processing, and order management.

## 🌟 Live Demo

**Access the live store at:** [Your Heroku/Railway URL after deployment]

## ✨ Features

- 🔐 **User Authentication** - OTP-based login system
- 🛒 **Shopping Cart** - Add, remove, update items
- 💳 **Payment Processing** - Multiple payment methods
- 📦 **Order Management** - Complete order lifecycle
- 📱 **Responsive Design** - Works on all devices
- 🗄️ **Database Support** - MySQL (production) / SQLite (demo)
- 🔍 **Product Search** - Find components easily
- 📊 **Order History** - View past orders

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- MySQL (optional - falls back to SQLite)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd robotech-store
   ```

2. **Start the application:**
   ```bash
   # macOS/Linux
   ./quick_start.sh

   # Windows
   start_project.bat

   # Manual start
   cd backend && python app.py
   ```

3. **Access the store:**
   - Frontend: http://localhost:7000
   - Backend API: http://localhost:8888

## 🌐 Deployment

### Option 1: Heroku (Recommended)

1. **Create Heroku account** at [heroku.com](https://heroku.com)

2. **Deploy automatically:**
   ```bash
   ./deploy.sh
   ```

3. **Or deploy manually:**
   ```bash
   heroku create your-store-name
   heroku addons:create jawsdb:kitefin
   git push heroku main
   heroku open
   ```

### Option 2: Railway

1. Connect your GitHub repo to [railway.app](https://railway.app)
2. Add MySQL database
3. Deploy automatically

### Option 3: Render

1. Connect repo to [render.com](https://render.com)
2. Add MySQL database
3. Deploy with provided settings

## 📋 API Endpoints

### Authentication
- `POST /api/send-otp` - Send OTP to phone
- `POST /api/verify-otp` - Verify OTP and login
- `GET /api/user/status` - Check login status

### Products
- `GET /api/products` - Get all products
- `GET /api/products?category=NAME` - Filter by category

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart` - Update cart item
- `DELETE /api/cart/:id` - Remove from cart

### Orders
- `GET /api/orders` - Get user's orders
- `POST /api/orders` - Create new order

## 🗂️ Project Structure

```
robotech-store/
├── backend/
│   ├── app.py              # Flask application
│   └── ...
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── Procfile               # Heroku deployment
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Database (auto-detected in production)
DATABASE_URL=mysql://user:pass@host:port/db

# Flask
FLASK_ENV=production
SECRET_KEY=your-secret-key

# CORS
FRONTEND_URL=https://your-domain.com
```

## 🧪 Testing

Test the deployment with:
- Login: Any phone number + OTP: `123456`
- Add products to cart
- Complete checkout
- View order history

## 📞 Support

For issues:
1. Check deployment logs
2. Verify environment variables
3. Test locally first

## 📄 License

This project is open source. Feel free to use and modify.

---

**Made with ❤️ for robotics enthusiasts**