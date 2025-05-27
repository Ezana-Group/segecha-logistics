# All models and db are now defined in database.py
# If you need to use models or db here, import them from database.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='Normal')
    alternative_contact_name = db.Column(db.String(100))
    alternative_contact_phone = db.Column(db.String(20))
    alternative_contact_email = db.Column(db.String(120))

    # Cargo Details
    cargo_description = db.Column(db.Text, nullable=False)
    cargo_type = db.Column(db.String(50), default='Standard')
    weight = db.Column(db.Float)
    weight_unit = db.Column(db.String(10), default='kg')
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    special_handling = db.Column(db.Text)

    # Shipping Details
    transport_method = db.Column(db.String(20), default='Road')
    status = db.Column(db.String(20), default='Pending')
    vehicle_plate = db.Column(db.String(20))
    pickup_date = db.Column(db.Date)
    pickup_time = db.Column(db.String(8))
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)

    # Insurance Details
    is_insured = db.Column(db.Boolean, default=False)
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    insurance_coverage_amount = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')

    # Additional Information
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)
    tags = db.Column(db.String(200))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Shipment, self).__init__(**kwargs)
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()

    def generate_tracking_id(self):
        prefix = 'SEG'
        timestamp = datetime.utcnow().strftime('%y%m%d')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{prefix}{timestamp}{random_suffix}"

    def calculate_volume(self):
        if all(x is not None for x in [self.length, self.width, self.height]):
            return self.length * self.width * self.height
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'tracking_id': self.tracking_id,
            'customer_name': self.customer_name,
            'priority': self.priority,
            'alternative_contact': {
                'name': self.alternative_contact_name,
                'phone': self.alternative_contact_phone,
                'email': self.alternative_contact_email
            },
            'cargo': {
                'description': self.cargo_description,
                'type': self.cargo_type,
                'weight': self.weight,
                'weight_unit': self.weight_unit,
                'dimensions': {
                    'length': self.length,
                    'width': self.width,
                    'height': self.height
                },
                'volume': self.calculate_volume(),
                'special_handling': self.special_handling
            },
            'shipping': {
                'method': self.transport_method,
                'status': self.status,
                'vehicle_plate': self.vehicle_plate,
                'pickup_date': self.pickup_date.isoformat() if self.pickup_date else None,
                'pickup_time': self.pickup_time,
                'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
                'actual_delivery': self.actual_delivery.isoformat() if self.actual_delivery else None
            },
            'insurance': {
                'is_insured': self.is_insured,
                'provider': self.insurance_provider,
                'policy_number': self.insurance_policy_number,
                'coverage_amount': self.insurance_coverage_amount,
                'currency': self.currency
            },
            'notes': self.notes,
            'internal_notes': self.internal_notes,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Shipment {self.tracking_id}>'

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_super_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100))
    
    # Pickup location details
    pickup_country = db.Column(db.String(100), nullable=False)
    pickup_city = db.Column(db.String(100), nullable=False)
    pickup_address = db.Column(db.String(200), nullable=False)
    pickup_lat = db.Column(db.Float, nullable=False)
    pickup_lng = db.Column(db.Float, nullable=False)
    pickup_display_name = db.Column(db.String(200))
    pickup_coordinates = db.Column(db.String(50))
    pickup_formatted_address = db.Column(db.String(200))
    
    # Dropoff location details
    dropoff_country = db.Column(db.String(100), nullable=False)
    dropoff_city = db.Column(db.String(100), nullable=False)
    dropoff_address = db.Column(db.String(200), nullable=False)
    dropoff_lat = db.Column(db.Float, nullable=False)
    dropoff_lng = db.Column(db.Float, nullable=False)
    dropoff_display_name = db.Column(db.String(200))
    dropoff_coordinates = db.Column(db.String(50))
    dropoff_formatted_address = db.Column(db.String(200))
    
    # Cargo and additional details
    cargo_description = db.Column(db.Text, nullable=False)
    preferred_date = db.Column(db.Date)
    additional_notes = db.Column(db.Text)
    estimated_distance = db.Column(db.Float)  # in kilometers
    
    # Status and timestamps
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    reviewer = db.relationship('User', backref='reviewed_quotes')
    shipment = db.relationship('Shipment', backref='quote_request', uselist=False)
    
    def __repr__(self):
        return f'<QuoteRequest {self.id}>'
    
    @property
    def pickup_location(self):
        return f"{self.pickup_address}, {self.pickup_city}, {self.pickup_country}"
    
    @property
    def dropoff_location(self):
        return f"{self.dropoff_address}, {self.dropoff_city}, {self.dropoff_country}" 