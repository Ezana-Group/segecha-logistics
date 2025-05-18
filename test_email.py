from flask import Flask
from flask_mail import Mail, Message
from config import Config

def test_email():
    # Create a test Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    
    try:
        with app.app_context():
            msg = Message(
                'Test Email from Segecha Logistics',
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[app.config['ADMIN_EMAIL']]  # Send to admin email for testing
            )
            msg.body = "This is a test email to verify the email configuration is working correctly."
            mail.send(msg)
            print("Test email sent successfully!")
            print(f"Sent from: {app.config['MAIL_DEFAULT_SENDER']}")
            print(f"Sent to: {app.config['ADMIN_EMAIL']}")
    except Exception as e:
        print(f"Error sending email: {e}")
        print("\nEmail Configuration:")
        print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
        print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
        print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
        print(f"MAIL_USERNAME: {'Set' if app.config['MAIL_USERNAME'] else 'Not Set'}")
        print(f"MAIL_PASSWORD: {'Set' if app.config['MAIL_PASSWORD'] else 'Not Set'}")
        print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")

if __name__ == '__main__':
    test_email() 