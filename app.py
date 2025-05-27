from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_migrate import Migrate
from datetime import datetime, timedelta
import requests
from config import Config
from database import db, Shipment, QuoteRequest
from cities import EAST_AFRICAN_CITIES
from flask_mail import Mail, Message
from commands import init_db_command
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
app.cli.add_command(init_db_command)

# Make config available in all templates
@app.context_processor
def inject_config():
    return dict(config=app.config)

OSRM_URL = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

@app.route('/')
def index():
    return render_template('index.html', now=datetime.now())

@app.route('/about')
def about():
    return render_template('about.html', now=datetime.now())

@app.route('/services')
def services():
    return render_template('services.html', now=datetime.now())

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy_policy.html', now=datetime.now())

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('legal/terms_of_service.html', now=datetime.now())

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('legal/cookie_policy.html', now=datetime.now())

def append_quote_to_sheet(quote_request):
    SERVICE_ACCOUNT_FILE = 'credentials/google-credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Gpye3QPcrwNOUojF4if4M3J2WNTwgGFT-nfao8m2Lhc/edit?gid=0')
    worksheet = sh.sheet1
    row = [
        str(quote_request.created_at),  # Date
        quote_request.name,  # Name
        quote_request.company,  # Company
        quote_request.email,  # Email
        quote_request.phone,  # Phone Number
        quote_request.pickup_location,  # Pickup Address
        f"{quote_request.pickup_lat:.6f},{quote_request.pickup_lng:.6f}",  # Pickup Coordinates
        quote_request.dropoff_location,  # Dropoff Address
        f"{quote_request.dropoff_lat:.6f},{quote_request.dropoff_lng:.6f}",  # Dropoff Coordinates
        quote_request.estimated_distance,  # Distance
        quote_request.cargo_description,  # Cargo description
        str(quote_request.preferred_date),  # Pick up Date
        quote_request.additional_notes,  # Notes
        ""  # Special Instruction (empty for now)
    ]
    print(f"Appending row to Google Sheet: {row}")  # Debug logging
    worksheet.append_row(row)

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
            append_quote_to_sheet(quote_request)
            send_confirmation_email(quote_request)
            return jsonify({'success': True, 'message': 'Quote submitted'})
        except Exception as e:
            print(f"Error processing quote: {e}")
            return jsonify({'success': False, 'message': 'Error'}), 500

    countries = list(EAST_AFRICAN_CITIES.keys())
    return render_template('quote.html', now=datetime.now(), countries=countries, EAST_AFRICAN_CITIES=EAST_AFRICAN_CITIES)

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        tracking_id = request.form.get('tracking_id')
        shipment = Shipment.query.filter_by(tracking_id=tracking_id).first()
        if shipment:
            return render_template('track.html', shipment=shipment, now=datetime.now(), show_result=True)
        flash('Tracking ID not found.', 'error')
    return render_template('track.html', now=datetime.now(), show_result=False)

@app.route('/get_cities/<country>')
def get_cities(country):
    return jsonify(list(EAST_AFRICAN_CITIES.get(country, {}).keys()))

@app.route('/get_city_coords/<country>/<city>')
def get_city_coords(country, city):
    return jsonify(EAST_AFRICAN_CITIES.get(country, {}).get(city, {}))

@app.route('/get_route_info/<float:start_lng>/<float:start_lat>/<float:end_lng>/<float:end_lat>')
def get_route_info(start_lng, start_lat, end_lng, end_lat):
    try:
        url = OSRM_URL.format(start_lng, start_lat, end_lng, end_lat)
        response = requests.get(url)
        data = response.json()
        if data['code'] == 'Ok' and data['routes']:
            route = data['routes'][0]
            return jsonify({
                'success': True,
                'distance': round(route['distance'] / 1000, 1),
                'duration': round(route['duration'] / 3600, 1),
                'geometry': route['geometry']
            })
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({'success': False, 'error': 'Route error'})

@app.route('/search_address')
def search_address():
    query = request.args.get('query', '')
    country = request.args.get('country', '')
    if not query:
        return jsonify([])
    params = {'q': query, 'format': 'json', 'limit': 5, 'addressdetails': 1}
    if country:
        params['country'] = country
    try:
        headers = {'User-Agent': 'Segecha Logistics Website'}
        response = requests.get(NOMINATIM_URL, params=params, headers=headers)
        results = response.json()
        addresses = [{
            'display_name': r['display_name'],
            'lat': float(r['lat']),
            'lon': float(r['lon']),
            'address': r.get('address', {})
        } for r in results]
        return jsonify(addresses)
    except Exception as e:
        print(f"Address search error: {e}")
        return jsonify([])

@app.route('/reverse_geocode')
def reverse_geocode():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if not lat or not lng:
        return jsonify({'error': 'Missing coordinates'}), 400
    try:
        headers = {'User-Agent': 'Segecha Logistics Website'}
        params = {
            'lat': lat,
            'lon': lng,
            'format': 'json',
            'addressdetails': 1
        }
        response = requests.get(NOMINATIM_REVERSE_URL, params=params, headers=headers)
        data = response.json()
        return jsonify({
            'display_name': data.get('display_name'),
            'address': data.get('address', {}),
            'lat': float(data.get('lat', lat)),
            'lon': float(data.get('lon', lng))
        })
    except Exception as e:
        print(f"Reverse geocoding error: {e}")
        return jsonify({'error': 'Reverse geocoding failed'}), 500

@app.route('/get_route')
def get_route():
    start_lng = request.args.get('start_lng')
    start_lat = request.args.get('start_lat')
    end_lng = request.args.get('end_lng')
    end_lat = request.args.get('end_lat')
    
    if not all([start_lng, start_lat, end_lng, end_lat]):
        return jsonify({'error': 'Missing coordinates'}), 400
    
    try:
        url = OSRM_URL.format(start_lng, start_lat, end_lng, end_lat)
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok' and data['routes']:
            route = data['routes'][0]
            return jsonify({
                'success': True,
                'distance': round(route['distance'] / 1000, 1),  # Convert to km
                'duration': round(route['duration'] / 3600, 1),  # Convert to hours
                'geometry': route['geometry']
            })
    except Exception as e:
        print(f"Route error: {e}")
    return jsonify({'error': 'Unable to get route'}), 500

def send_confirmation_email(quote_request):
    try:
        # Send to the customer
        msg = Message('Quote Request Confirmation - Segecha Logistics',
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[quote_request.email])
        msg.html = render_template(
            'email/quote_confirmation.html',
            quote=quote_request,
            name=quote_request.name,
            now=datetime.utcnow()
        )
        mail.send(msg)

        # Always send a copy to segechagroup@gmail.com
        admin_msg = Message('New Quote Request - Segecha Logistics',
                          sender=app.config['MAIL_DEFAULT_SENDER'],
                          recipients=['segechagroup@gmail.com'])
        admin_msg.html = render_template(
            'email/quote_admin_notification.html',
            quote=quote_request,
            now=datetime.utcnow()
        )
        mail.send(admin_msg)
    except Exception as e:
        print(f"Email send error: {e}")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Send email notification
            msg = Message('New Contact Form Submission - Segecha Logistics',
                         sender=app.config['MAIL_DEFAULT_SENDER'],
                         recipients=['segechagroup@gmail.com'])
            msg.html = render_template(
                'email/contact_notification.html',
                name=request.form['name'],
                email=request.form['email'],
                phone=request.form['phone'],
                message=request.form['message'],
                now=datetime.utcnow()
            )
            mail.send(msg)
            flash('Thank you for your message. We will get back to you soon!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            print(f"Error sending contact form: {e}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
            return redirect(url_for('contact'))
    return render_template('contact.html', now=datetime.now())

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)
