#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
echo "Installing required system packages..."
sudo apt-get install -y python3-pip python3-venv nginx postgresql postgresql-contrib

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up PostgreSQL
echo "Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE segecha;"
sudo -u postgres psql -c "CREATE USER segecha WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE segecha TO segecha;"

# Set up Nginx
echo "Configuring Nginx..."
sudo cp nginx/segecha.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/segecha.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Set up SSL with Let's Encrypt
echo "Setting up SSL certificate..."
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# Create systemd service
echo "Setting up systemd service..."
sudo cp systemd/segecha.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable segecha
sudo systemctl start segecha

# Restart Nginx
echo "Restarting Nginx..."
sudo systemctl restart nginx

echo "Deployment completed successfully!" 