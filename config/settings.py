"""
Segecha Logistics Configuration Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email Configuration
EMAIL_CONFIG = {
    'SMTP_HOST': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'SMTP_PORT': int(os.getenv('SMTP_PORT', 587)),
    'SMTP_USERNAME': os.getenv('SMTP_USERNAME', 'your-email@gmail.com'),
    'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD', 'your-app-password'),
    'SENDER_EMAIL': os.getenv('SENDER_EMAIL', 'noreply@segecha.com'),
    'USE_TLS': True
}

# Business Contact Information
CONTACT_INFO = {
    'PHONES': [
        os.getenv('BUSINESS_PHONE_1', '+254 XXX XXX XXX'),
        os.getenv('BUSINESS_PHONE_2', '+254 XXX XXX XXX')
    ],
    'EMAILS': {
        'info': os.getenv('BUSINESS_EMAIL_INFO', 'info@segecha.com'),
        'support': os.getenv('BUSINESS_EMAIL_SUPPORT', 'support@segecha.com'),
        'quotes': os.getenv('BUSINESS_EMAIL_QUOTES', 'quotes@segecha.com')
    },
    'ADDRESS': os.getenv('BUSINESS_ADDRESS', 'Your Business Address, Nairobi, Kenya')
}

# Map Services Configuration
MAP_CONFIG = {
    'provider': 'openstreetmap',  # or 'google' if using Google Maps
    'google_maps_api_key': os.getenv('GOOGLE_MAPS_API_KEY', ''),
    'google_places_api_key': os.getenv('GOOGLE_PLACES_API_KEY', '')
}

# Optional Third-party Services
SERVICES = {
    'sms': {
        'api_key': os.getenv('SMS_API_KEY', ''),
        'sender_id': os.getenv('SMS_SENDER_ID', 'SEGECHA')
    },
    'payment': {
        'gateway_key': os.getenv('PAYMENT_GATEWAY_KEY', '')
    },
    'analytics': {
        'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', '')
    }
}

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'generate-a-secure-secret-key')

# Email Templates Directory
EMAIL_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates/emails')

# Quote Request Email Template
QUOTE_REQUEST_EMAIL_TEMPLATE = """
Dear {name},

Thank you for requesting a quote from Segecha Logistics. We have received your request with the following details:

Pickup Location: {pickup_location}
Delivery Location: {delivery_location}
Cargo Description: {cargo_description}
Preferred Date: {preferred_date}

Our team will review your request and get back to you within 24 hours with a detailed quote.

If you have any questions, please don't hesitate to contact us:
Phone: {business_phone}
Email: {business_email}

Best regards,
Segecha Logistics Team
"""

# Quote Admin Notification Template
QUOTE_ADMIN_NOTIFICATION_TEMPLATE = """
New Quote Request Received

Customer Details:
Name: {name}
Company: {company}
Email: {email}
Phone: {phone}

Shipment Details:
Pickup: {pickup_location}
Delivery: {delivery_location}
Cargo: {cargo_description}
Preferred Date: {preferred_date}

Please review and prepare a quote.
""" 