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
from flask import make_response, send_from_directory, request
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)

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

# Helper routes and public pages...

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

@app.after_request
def add_cache_control(response):
    if request.path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

if __name__ == '__main__':
    with app.app_context():
        from flask_migrate import upgrade
        from database import Admin
        upgrade()
        if not Admin.query.filter_by(email="admin@segecha.com").first():
            admin = Admin(email="admin@segecha.com")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created.")
        else:
            print("ℹ️ Admin user already exists.")
    app.run(host="0.0.0.0", port=10000, debug=True)
