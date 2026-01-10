#!/bin/bash

# Robotech Store - One-Click Deployment Script
# This script helps deploy your store to Heroku

echo "🚀 Robotech Store Deployment Helper"
echo "==================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "Install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "Please login to Heroku first:"
    heroku login
fi

echo "Enter your app name (this will be your store's URL):"
read -r APP_NAME

echo "Creating Heroku app: $APP_NAME"
heroku create "$APP_NAME"

echo "Adding MySQL database (JawsDB)..."
heroku addons:create jawsdb:kitefin -a "$APP_NAME"

echo "Setting environment variables..."
heroku config:set FLASK_ENV=production -a "$APP_NAME"
heroku config:set SECRET_KEY="$(openssl rand -hex 32)" -a "$APP_NAME"

echo "Deploying your code..."
git add .
git commit -m "Deploy to production"
git push heroku main

echo ""
echo "🎉 Deployment Complete!"
echo "Your store is live at: https://$APP_NAME.herokuapp.com"
echo ""
echo "Test it out:"
echo "• Visit: https://$APP_NAME.herokuapp.com"
echo "• Login with any phone number + OTP: 123456"
echo "• Add products to cart and place orders!"
echo ""
echo "To view logs: heroku logs --tail -a $APP_NAME"
