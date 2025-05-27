import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length=32):
    """Generate a random secret key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Create .env file with default values."""
    env_content = f"""# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY={generate_secret_key()}

# Database Configuration
DATABASE_URL=postgresql://segecha:your_password@localhost:5432/segecha_logistics

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Admin Configuration
ADMIN_EMAIL=admin@segecha.com
ADMIN_PASSWORD=your-secure-password

# WhatsApp Configuration
WHATSAPP_NUMBER=254XXXXXXXXX

# Payment Integration (M-Pesa)
MPESA_CONSUMER_KEY=your-consumer-key
MPESA_CONSUMER_SECRET=your-consumer-secret
MPESA_PASSKEY=your-passkey
MPESA_SHORTCODE=your-shortcode
MPESA_CALLBACK_URL=your-callback-url

# Map Services
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
OPENCAGE_API_KEY=your-opencage-api-key
OSRM_API_URL=your-osrm-api-url

# SMS Gateway
SMS_API_KEY=your-sms-api-key
SMS_SENDER_ID=your-sender-id

# Security
JWT_SECRET_KEY={generate_secret_key()}
PASSWORD_SALT={generate_secret_key()}

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Backup Configuration
BACKUP_DIR=backups
BACKUP_RETENTION_DAYS=30
"""
    
    # Create necessary directories
    Path('logs').mkdir(exist_ok=True)
    Path('backups').mkdir(exist_ok=True)
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Created .env file with default values. Please update the values with your actual configuration.")

if __name__ == '__main__':
    create_env_file() 