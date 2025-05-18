from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests
from config import Config
from database import db, Admin, QuoteRequest, Shipment
from cities import EAST_AFRICAN_CITIES
from flask_mail import Mail, Message
from commands import init_db_command

app = Flask(__name__)
app.config.from_object(Config)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Initialize Flask-Mail
mail = Mail(app)

# Register commands
app.cli.add_command(init_db_command)

# OSRM service URL
OSRM_URL = "https://router.project-osrm.org/route/v1/driving/{},{};{},{}"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Helper route for getting cities
@app.route('/get_cities/<country>')
def get_cities(country):
    if country in EAST_AFRICAN_CITIES:
        return jsonify(list(EAST_AFRICAN_CITIES[country].keys()))
    return jsonify([])

# Helper route for getting city coordinates
@app.route('/get_city_coords/<country>/<city>')
def get_city_coords(country, city):
    if country in EAST_AFRICAN_CITIES and city in EAST_AFRICAN_CITIES[country]:
        return jsonify(EAST_AFRICAN_CITIES[country][city])
    return jsonify({})

# Public routes
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
            # Convert preferred_date string to date object if provided
            preferred_date = None
            if request.form.get('preferred_date'):
                preferred_date = datetime.strptime(request.form.get('preferred_date'), '%Y-%m-%d').date()

            # Build location strings
            pickup_location = f"{request.form.get('pickup_address')}, {request.form.get('pickup_city')}, {request.form.get('pickup_country')}"
            dropoff_location = f"{request.form.get('dropoff_address')}, {request.form.get('dropoff_city')}, {request.form.get('dropoff_country')}"

            # Get coordinates and distance
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
            
            # Send confirmation email
            send_confirmation_email(quote_request)
            
            # Return success response for AJAX
            return jsonify({
                'success': True,
                'message': 'Your quote request has been submitted successfully!'
            })
            
        except Exception as e:
            print(f"Error processing quote request: {e}")
            return jsonify({
                'success': False,
                'message': 'An error occurred while processing your request. Please try again.'
            }), 500
    
    # Pass both the countries list and the full cities data to the template
    countries = list(EAST_AFRICAN_CITIES.keys())
    return render_template('quote.html', 
                         now=datetime.now(), 
                         countries=countries,
                         EAST_AFRICAN_CITIES=EAST_AFRICAN_CITIES)

@app.route('/contact')
def contact():
    return render_template('contact.html', now=datetime.now())

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        admin = Admin.query.filter_by(email=request.form['email']).first()
        if admin and admin.check_password(request.form['password']):
            login_user(admin)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('admin_login.html', now=datetime.now())

@app.route('/admin')
@login_required
def admin_dashboard():
    quote_requests = QuoteRequest.query.order_by(QuoteRequest.created_at.desc()).all()
    # Get the 5 most recent shipments
    recent_shipments = Shipment.query.order_by(Shipment.created_at.desc()).limit(5).all()
    return render_template('admin_dashboard.html', 
                         quote_requests=quote_requests, 
                         recent_shipments=recent_shipments,
                         now=datetime.now())

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/mark_reviewed/<int:quote_id>', methods=['POST'])
@login_required
def mark_reviewed(quote_id):
    quote_request = QuoteRequest.query.get_or_404(quote_id)
    quote_request.reviewed = not quote_request.reviewed
    db.session.commit()
    return jsonify({'success': True, 'reviewed': quote_request.reviewed})

@app.route('/get_route_info/<float:start_lng>/<float:start_lat>/<float:end_lng>/<float:end_lat>')
def get_route_info(start_lng, start_lat, end_lng, end_lat):
    try:
        # Call OSRM service
        url = OSRM_URL.format(start_lng, start_lat, end_lng, end_lat)
        response = requests.get(url)
        data = response.json()
        
        if data['code'] == 'Ok' and len(data['routes']) > 0:
            route = data['routes'][0]
            
            # Extract relevant information
            distance_km = round(route['distance'] / 1000, 1)  # Convert meters to km
            duration_hours = round(route['duration'] / 3600, 1)  # Convert seconds to hours
            
            # Get route geometry for visualization
            geometry = route['geometry']
            
            return jsonify({
                'success': True,
                'distance': distance_km,
                'duration': duration_hours,
                'geometry': geometry
            })
    except Exception as e:
        print(f"Error getting route info: {e}")
    
    return jsonify({
        'success': False,
        'error': 'Unable to calculate route'
    })

@app.route('/search_address')
def search_address():
    query = request.args.get('query', '')
    country = request.args.get('country', '')
    
    if not query:
        return jsonify([])
    
    # Call Nominatim API with country filter if provided
    params = {
        'q': query,
        'format': 'json',
        'limit': 5,
        'addressdetails': 1
    }
    
    if country:
        params['country'] = country
    
    try:
        headers = {'User-Agent': 'Segecha Logistics Website'}
        response = requests.get(NOMINATIM_URL, params=params, headers=headers)
        results = response.json()
        
        # Format results
        addresses = []
        for result in results:
            address = {
                'display_name': result['display_name'],
                'lat': float(result['lat']),
                'lon': float(result['lon']),
                'address': result.get('address', {})
            }
            addresses.append(address)
        
        return jsonify(addresses)
    except Exception as e:
        print(f"Error in address search: {e}")
        return jsonify([])

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy_policy.html', now=datetime.now())

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('legal/terms_of_service.html', now=datetime.now())

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('legal/cookie_policy.html', now=datetime.now())

@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        tracking_id = request.form.get('tracking_id')
        shipment = Shipment.query.filter_by(tracking_id=tracking_id).first()
        if shipment:
            return render_template('track.html', 
                                shipment=shipment, 
                                now=datetime.now(),
                                show_result=True)
        flash('Tracking ID not found. Please check and try again.', 'error')
    return render_template('track.html', now=datetime.now(), show_result=False)

@app.route('/admin/shipments')
@login_required
def admin_shipments():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Shipment.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                Shipment.tracking_id.ilike(f'%{search}%'),
                Shipment.customer_name.ilike(f'%{search}%'),
                Shipment.cargo_description.ilike(f'%{search}%')
            )
        )
    
    shipments = query.order_by(Shipment.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/admin_shipments.html', 
                         shipments=shipments,
                         status_filter=status_filter,
                         search=search,
                         now=datetime.now())

@app.route('/admin/shipment/new', methods=['GET', 'POST'])
@login_required
def new_shipment():
    if request.method == 'POST':
        try:
            # Parse pickup date and time if provided
            pickup_date = None
            if request.form.get('pickup_date'):
                pickup_date = datetime.strptime(request.form['pickup_date'], '%Y-%m-%d')
                if request.form.get('pickup_time'):
                    time_parts = request.form['pickup_time'].split(':')
                    pickup_date = pickup_date.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))

            shipment = Shipment(
                customer_name=request.form['customer_name'],
                pickup_location=request.form['pickup_location'],
                pickup_lat=float(request.form.get('pickup_lat', 0)),
                pickup_lng=float(request.form.get('pickup_lng', 0)),
                dropoff_location=request.form['dropoff_location'],
                dropoff_lat=float(request.form.get('dropoff_lat', 0)),
                dropoff_lng=float(request.form.get('dropoff_lng', 0)),
                cargo_description=request.form['cargo_description'],
                status=request.form['status'],
                current_location=request.form.get('current_location'),
                current_lat=float(request.form.get('current_lat', 0)),
                current_lng=float(request.form.get('current_lng', 0)),
                estimated_delivery=datetime.strptime(request.form['estimated_delivery'], '%Y-%m-%dT%H:%M'),
                notes=request.form.get('notes'),
                # New pickup fields
                pickup_date=pickup_date,
                pickup_time=request.form.get('pickup_time'),
                vehicle_plate=request.form.get('vehicle_plate'),
                pickup_status=request.form.get('pickup_status', 'Pending'),
                pickup_notes=request.form.get('pickup_notes')
            )
            
            quote_request_id = request.form.get('quote_request_id')
            if quote_request_id:
                quote_request = QuoteRequest.query.get(quote_request_id)
                if quote_request:
                    shipment.quote_request = quote_request
            
            db.session.add(shipment)
            db.session.commit()
            flash('Shipment created successfully.', 'success')
            return redirect(url_for('admin_shipments'))
        except Exception as e:
            flash('Error creating shipment. Please try again.', 'error')
            print(e)
    
    quote_request_id = request.args.get('quote_request_id')
    quote_request = None
    if quote_request_id:
        quote_request = QuoteRequest.query.get(quote_request_id)
    
    return render_template('admin/shipment_form.html', 
                         shipment=None,
                         quote_request=quote_request,
                         now=datetime.now())

@app.route('/admin/shipment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Parse pickup date and time if provided
            if request.form.get('pickup_date'):
                pickup_date = datetime.strptime(request.form['pickup_date'], '%Y-%m-%d')
                if request.form.get('pickup_time'):
                    time_parts = request.form['pickup_time'].split(':')
                    pickup_date = pickup_date.replace(hour=int(time_parts[0]), minute=int(time_parts[1]))
                shipment.pickup_date = pickup_date
            
            shipment.customer_name = request.form['customer_name']
            shipment.pickup_location = request.form['pickup_location']
            shipment.pickup_lat = float(request.form.get('pickup_lat', 0))
            shipment.pickup_lng = float(request.form.get('pickup_lng', 0))
            shipment.dropoff_location = request.form['dropoff_location']
            shipment.dropoff_lat = float(request.form.get('dropoff_lat', 0))
            shipment.dropoff_lng = float(request.form.get('dropoff_lng', 0))
            shipment.cargo_description = request.form['cargo_description']
            shipment.status = request.form['status']
            shipment.current_location = request.form.get('current_location')
            shipment.current_lat = float(request.form.get('current_lat', 0))
            shipment.current_lng = float(request.form.get('current_lng', 0))
            shipment.estimated_delivery = datetime.strptime(request.form['estimated_delivery'], '%Y-%m-%dT%H:%M')
            shipment.notes = request.form.get('notes')
            
            # Update pickup details
            shipment.pickup_time = request.form.get('pickup_time')
            shipment.vehicle_plate = request.form.get('vehicle_plate')
            shipment.pickup_status = request.form.get('pickup_status', 'Pending')
            shipment.pickup_notes = request.form.get('pickup_notes')
            
            db.session.commit()
            flash('Shipment updated successfully.', 'success')
            return redirect(url_for('admin_shipments'))
        except Exception as e:
            flash('Error updating shipment. Please try again.', 'error')
            print(e)
    
    return render_template('admin/shipment_form.html', 
                         shipment=shipment,
                         quote_request=shipment.quote_request,
                         now=datetime.now())

@app.route('/admin/shipment/delete/<int:id>', methods=['POST'])
@login_required
def delete_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    try:
        db.session.delete(shipment)
        db.session.commit()
        flash('Shipment deleted successfully.', 'success')
    except:
        flash('Error deleting shipment.', 'error')
    return redirect(url_for('admin_shipments'))

@app.route('/admin/shipment/mark-delivered/<int:id>', methods=['POST'])
@login_required
def mark_shipment_delivered(id):
    shipment = Shipment.query.get_or_404(id)
    try:
        shipment.status = 'Delivered'
        db.session.commit()
        flash('Shipment marked as delivered.', 'success')
    except:
        flash('Error updating shipment status.', 'error')
    return redirect(url_for('admin_shipments'))

if __name__ == '__main__':
    app.run(debug=True) 