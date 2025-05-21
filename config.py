import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use absolute path for database
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/mose/segecha_logistics/instance/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin credentials
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@segecha.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # Email config
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'segechagroup@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@segecha.com')
    
    # Contact Information
    CONTACT_PHONE_1 = '+254 721 762 828'
    CONTACT_PHONE_2 = '+254 107 971 792'
    CONTACT_EMAIL = 'info@segecha.com'  # Display email
    CONTACT_EMAIL_FORWARD = 'segechagroup@gmail.com'  # Actual receiving email
    CONTACT_ADDRESS = 'Mombasa Port, Shed 12, Port Reitz Road, Mombasa, Kenya'
    CONTACT_BUSINESS_HOURS = {
        'weekdays': 'Monday - Friday: 8:00 AM - 6:00 PM',
        'saturday': 'Saturday: 9:00 AM - 2:00 PM',
        'sunday': 'Sunday: Closed'
    }
    
    # Social Media (placeholder URLs - update when available)
    SOCIAL_MEDIA = {
        'facebook': '#',  # Update when available
        'twitter': '#',   # Update when available
        'instagram': '#', # Update when available
        'linkedin': '#'   # Update when available
    }
    
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '254107971792'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)