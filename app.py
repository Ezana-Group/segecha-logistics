from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests
from config import Config
from database import db, QuoteRequest, Shipment
from cities import EAST_AFRICAN_CITIES
from flask_mail import Mail, Message
from commands import init_db_command
from flask import make_response, send_from_directory

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Initialize Flask-Mail
mail = Mail(app)

# Register commands
app.cli.add_command(init_db_command)

# OSRM service URL
OSRM_URL = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

@app.route('/')
def index():
    return render_template('index.html', now=datetime.now())

@app.route('/about')
def about():
    return render_template('about.html', now=datetime.now())

@app.route('/services')
def services():
    return render_template('services.html', now=datetime.now())

def send_confirmation_email(quote_request):
    try:
        msg = Message(
            'Your Quote Request Confirmation - Segecha Logistics',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[quote_request.email]
        )
        msg.html = render_template(
            'email/quote_confirmation.html',
            quote=quote_request,
            name=quote_request.name
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error sending confirmation email: {e}")

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        try:
            preferred_date = None
            if request.form.get('preferred_date'):
                preferred_date = datetime.strptime(request.form.get('preferred_date'), '%Y-%m-%d').date()

            pickup_location = f"{request.form.get('pickup_address')}, {request.form.get('pickup_city')}, {request.form.get('pickup_country')}"
            dropoff_location = f"{request.form.get('dropoff_address')}, {request.form.get('dropoff_city')}, {request.form.get('dropoff_country')}"
            pickup_lat = float(request.form.get('pickup_lat', 0))
            pickup_lng = float(request.form.get('pickup_lng', 0))
            dropoff_lat = float(request.form.get('dropoff_lat', 0))
            dropoff_lng = float(request.form.get('dropoff_lng', 0))
            estimated_distance = float(request.form.get('estimated_distance', 0))

            quote_request = QuoteRequest(
                name=request.form['name'],
                company=request.form.get('company'),
                email=request.form['email'],
                phone=request.form['phone'],
                pickup_location=pickup_location,
                pickup_lat=pickup_lat,
                pickup_lng=pickup_lng,
                dropoff_location=dropoff_location,
                dropoff_lat=dropoff_lat,
                dropoff_lng=dropoff_lng,
                estimated_distance=estimated_distance,
                cargo_description=request.form['cargo_description'],
                preferred_date=preferred_date,
                additional_notes=request.form.get('additional_notes')
            )
            db.session.add(quote_request)
            db.session.commit()
            send_confirmation_email(quote_request)
            return jsonify({'success': True, 'message': 'Your quote request has been submitted successfully!'})
        except Exception as e:
            print(f"Error processing quote request: {e}")
            return jsonify({'success': False, 'message': 'An error occurred while processing your request.'}), 500

    countries = list(EAST_AFRICAN_CITIES.keys())
    return render_template('quote.html', now=datetime.now(), countries=countries, EAST_AFRICAN_CITIES=EAST_AFRICAN_CITIES)

@app.route('/contact')
def contact():
    return render_template('contact.html', now=datetime.now())

@app.route('/admin')
def admin_dashboard():
    quote_requests = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
    recent_shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html', quote_requests=quote_requests, recent_shipments=recent_shipments, now=datetime.now())

@app.after_request
def add_cache_control(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

if __name__ == '__main__':
    with app.app_context():
        from flask_migrate import upgrade
        upgrade()
    app.run(host="0.0.0.0", port=10000, debug=True)
