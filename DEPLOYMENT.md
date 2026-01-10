# 🚀 Robotech Store Deployment Guide

This guide will help you deploy your Robotech Store to make it accessible online via a link, even when you close your terminal and Cursor.

## 🎯 Deployment Options

### **Option 1: Heroku (Recommended - Free & Easy)**

#### Step 1: Create a Heroku Account
1. Go to [heroku.com](https://heroku.com) and sign up
2. Install Heroku CLI: `brew install heroku` (macOS) or download from website

#### Step 2: Prepare Your Code
Your repository is already prepared with:
- ✅ `requirements.txt` with production dependencies
- ✅ `Procfile` for Heroku
- ✅ `runtime.txt` for Python version
- ✅ Production-ready CORS configuration

#### Step 3: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-robotech-store

# Add MySQL database (JawsDB is free)
heroku addons:create jawsdb:kitefin

# Push your code to Heroku
git add .
git commit -m "Ready for deployment"
git push heroku main

# Open your live store
heroku open
```

#### Step 4: Set Environment Variables
```bash
# Set Flask environment to production
heroku config:set FLASK_ENV=production

# Set a secret key (generate a random string)
heroku config:set SECRET_KEY=your-random-secret-key-here
```

### **Option 2: Railway (Modern Alternative)**

#### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app) and sign up
2. Connect your GitHub repository

#### Step 2: Add Database
1. Add a MySQL database from the Railway dashboard
2. Copy the database URL from Railway environment variables

#### Step 3: Deploy
Railway will automatically detect your Flask app and deploy it. The `Procfile` and `requirements.txt` will handle the configuration.

### **Option 3: Render (Free Tier Available)**

#### Step 1: Create Render Account
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub repository

#### Step 2: Create Web Service
1. Create a new Web Service
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

#### Step 3: Add Database
1. Create a MySQL database on Render
2. Copy the database URL to environment variables

## 🔧 Environment Variables Required

For production deployment, set these environment variables:

```
FLASK_ENV=production
DATABASE_URL=mysql://username:password@host:port/database_name
SECRET_KEY=your-random-secret-key-here
FRONTEND_URL=https://your-app-name.herokuapp.com
```

## 🗄️ Database Setup

### For Heroku with JawsDB:
```bash
# After deployment, the DATABASE_URL will be automatically set
# Your app will automatically parse this URL
```

### For Local Testing:
```bash
# Create .env file with local database settings
cp env.example .env
# Edit .env with your local MySQL credentials
```

## 🌐 Your Live Store URLs

After deployment, your store will be available at:
- **Main Store**: `https://your-app-name.herokuapp.com/`
- **Products**: `https://your-app-name.herokuapp.com/products`
- **Cart**: `https://your-app-name.herokuapp.com/cart`
- **Orders**: `https://your-app-name.herokuapp.com/orders`

## 📋 Features That Will Work Online

✅ **User Authentication** - OTP login system
✅ **Product Catalog** - All 60 products with images
✅ **Shopping Cart** - Add, remove, update items
✅ **Order Processing** - Complete checkout flow
✅ **Order History** - View past orders
✅ **Payment Processing** - Mock payment system
✅ **Responsive Design** - Works on mobile and desktop

## 🔍 Testing Your Deployment

1. **Visit your live URL**
2. **Try the login system** (use any phone number with OTP 123456)
3. **Add products to cart**
4. **Complete an order**
5. **View order history**

## 💰 Free Tiers Available

- **Heroku**: 550 free hours/month
- **Railway**: $5/month credit for new users
- **Render**: 750 free hours/month
- **PlanetScale**: Free MySQL database tier

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Check Heroku logs
heroku logs --tail

# Check Railway logs in dashboard
# Check Render logs in dashboard
```

### CORS Issues
- Make sure `FLASK_ENV=production` is set
- The app automatically allows all origins in production

### Static Files Not Loading
- Flask serves static files automatically
- Check that `static/` folder is in your repository

## 📞 Support

If you encounter issues:
1. Check the deployment platform's logs
2. Verify environment variables are set correctly
3. Test locally first with `./quick_start.sh`

## 🎉 You're Done!

Once deployed, share your store's URL and anyone can:
- Browse products
- Create accounts
- Add items to cart
- Place orders
- View order history

Your Robotech Store is now live and accessible worldwide! 🌟
