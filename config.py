import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Original Version
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \ 
        #'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')

    uri = os.environ.get('DATABASE_URL', '').replace("postgres://", "postgresql://")
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Admin credentials (should be moved to environment variables in production)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@segecha.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'  # Change in production!
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'info@segecha.com')
    
    # WhatsApp number
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER') or '254700000000'  # Replace with actual number 
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)