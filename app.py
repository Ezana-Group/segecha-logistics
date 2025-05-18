from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_migrate import Migrate
from datetime import datetime
import requests
from config import Config
from database import db, QuoteRequest, Shipment
from cities import EAST_AFRICAN_CITIES
from flask_mail import Mail, Message
from commands import init_db_command

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)
app.cli.add_command(init_db_command)

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

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy_policy.html', now=datetime.now())

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('legal/terms_of_service.html', now=datetime.now())

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('legal/cookie_policy.html', now=datetime.now())

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

def send_confirmation_email(quote_request):
    try:
        msg = Message('Quote Request Confirmation - Segecha Logistics',
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[quote_request.email])
        msg.html = render_template('email/quote_confirmation.html', quote=quote_request, name=quote_request.name)
        mail.send(msg)
    except Exception as e:
        print(f"Email send error: {e}")

@app.route('/contact')
def contact():
    return render_template('contact.html', now=datetime.now())

@app.after_request
def add_cache_control(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/admin')
def admin_dashboard():
    quote_requests = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
    recent_shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html', now=datetime.now(), quote_requests=quote_requests, recent_shipments=recent_shipments)

@app.route('/test')
def test():
    return "Test route is working!"

@app.route('/admin/shipments')
def admin_shipments():
    shipments = Shipment.query.order_by(Shipment.created_at.desc()).all()
    return render_template('admin/admin_shipments.html', shipments=shipments, now=datetime.now())

@app.route('/admin/new-shipment', methods=['GET', 'POST'])
def new_shipment():
    if request.method == 'POST':
        try:
            # Parse dates
            pickup_date = None
            if request.form.get('pickup_date'):
                pickup_date = datetime.strptime(request.form.get('pickup_date'), '%Y-%m-%d')
            
            estimated_delivery = None
            if request.form.get('estimated_delivery'):
                estimated_delivery = datetime.strptime(request.form.get('estimated_delivery'), '%Y-%m-%dT%H:%M')

            # Create new shipment
            shipment = Shipment(
                customer_name=request.form['customer_name'],
                pickup_location=request.form['pickup_location'],
                pickup_lat=float(request.form.get('pickup_lat', 0)),
                pickup_lng=float(request.form.get('pickup_lng', 0)),
                dropoff_location=request.form['dropoff_location'],
                dropoff_lat=float(request.form.get('dropoff_lat', 0)),
                dropoff_lng=float(request.form.get('dropoff_lng', 0)),
                cargo_description=request.form['cargo_description'],
                pickup_date=pickup_date,
                pickup_time=request.form.get('pickup_time'),
                vehicle_plate=request.form.get('vehicle_plate'),
                pickup_status=request.form.get('pickup_status', 'Pending'),
                pickup_notes=request.form.get('pickup_notes'),
                status=request.form.get('status', 'Pending'),
                estimated_delivery=estimated_delivery,
                notes=request.form.get('notes')
            )
            
            db.session.add(shipment)
            db.session.commit()
            
            flash('Shipment created successfully!', 'success')
            return redirect(url_for('admin_shipments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating shipment: {str(e)}', 'error')
            return redirect(url_for('new_shipment'))
            
    return render_template('admin/shipment_form.html', shipment=None, quote_request=None, now=datetime.now())

@app.route('/admin/edit-shipment/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Parse dates
            pickup_date = None
            if request.form.get('pickup_date'):
                pickup_date = datetime.strptime(request.form.get('pickup_date'), '%Y-%m-%d')
            
            estimated_delivery = None
            if request.form.get('estimated_delivery'):
                estimated_delivery = datetime.strptime(request.form.get('estimated_delivery'), '%Y-%m-%dT%H:%M')

            # Update shipment
            shipment.customer_name = request.form['customer_name']
            shipment.pickup_location = request.form['pickup_location']
            shipment.pickup_lat = float(request.form.get('pickup_lat', 0))
            shipment.pickup_lng = float(request.form.get('pickup_lng', 0))
            shipment.dropoff_location = request.form['dropoff_location']
            shipment.dropoff_lat = float(request.form.get('dropoff_lat', 0))
            shipment.dropoff_lng = float(request.form.get('dropoff_lng', 0))
            shipment.cargo_description = request.form['cargo_description']
            shipment.pickup_date = pickup_date
            shipment.pickup_time = request.form.get('pickup_time')
            shipment.vehicle_plate = request.form.get('vehicle_plate')
            shipment.pickup_status = request.form.get('pickup_status', 'Pending')
            shipment.pickup_notes = request.form.get('pickup_notes')
            shipment.status = request.form.get('status', 'Pending')
            shipment.estimated_delivery = estimated_delivery
            shipment.notes = request.form.get('notes')
            
            db.session.commit()
            flash('Shipment updated successfully!', 'success')
            return redirect(url_for('admin_shipments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating shipment: {str(e)}', 'error')
            return redirect(url_for('edit_shipment', id=id))
    
    return render_template('admin/shipment_form.html', shipment=shipment, quote_request=None, now=datetime.now())

@app.route('/admin/mark-shipment-delivered/<int:id>', methods=['POST'])
def mark_shipment_delivered(id):
    shipment = Shipment.query.get_or_404(id)
    try:
        shipment.status = 'Delivered'
        shipment.actual_delivery = datetime.utcnow()
        db.session.commit()
        flash('Shipment marked as delivered!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking shipment as delivered: {str(e)}', 'error')
    return redirect(url_for('admin_shipments'))

@app.route('/admin/delete-shipment/<int:id>', methods=['POST'])
def delete_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    try:
        db.session.delete(shipment)
        db.session.commit()
        flash('Shipment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting shipment: {str(e)}', 'error')
    return redirect(url_for('admin_shipments'))

@app.route('/admin/new-quote', methods=['GET', 'POST'])
def admin_new_quote():
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
                additional_notes=request.form.get('additional_notes'),
                reviewed=True  # Mark as reviewed since it's created by admin
            )
            db.session.add(quote_request)
            db.session.commit()
            
            # Optionally create a shipment directly from this quote
            if request.form.get('create_shipment') == 'yes':
                shipment = Shipment(
                    quote_request_id=quote_request.id,
                    customer_name=quote_request.name,
                    pickup_location=quote_request.pickup_location,
                    pickup_lat=quote_request.pickup_lat,
                    pickup_lng=quote_request.pickup_lng,
                    dropoff_location=quote_request.dropoff_location,
                    dropoff_lat=quote_request.dropoff_lat,
                    dropoff_lng=quote_request.dropoff_lng,
                    cargo_description=quote_request.cargo_description,
                    status='Pending'
                )
                db.session.add(shipment)
                db.session.commit()
                flash('Quote created and shipment initiated!', 'success')
                return redirect(url_for('admin_shipments'))
            
            flash('Quote created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating quote: {str(e)}', 'error')
            return redirect(url_for('admin_new_quote'))
    
    countries = list(EAST_AFRICAN_CITIES.keys())
    return render_template('admin/new_quote.html', 
                         now=datetime.now(), 
                         countries=countries, 
                         EAST_AFRICAN_CITIES=EAST_AFRICAN_CITIES)

# Remove or comment out the /admin_login route and any related logic
# @app.route('/admin_login', methods=['GET', 'POST'])
# def admin_login():
#     ...

if __name__ == '__main__':
    app.run(debug=True, port=10000)
