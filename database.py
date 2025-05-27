from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    dropoff_location = db.Column(db.String(200), nullable=False)
    dropoff_lat = db.Column(db.Float)
    dropoff_lng = db.Column(db.Float)
    estimated_distance = db.Column(db.Float)  # Distance in kilometers
    cargo_description = db.Column(db.Text, nullable=False)
    preferred_date = db.Column(db.Date)
    additional_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False)
    # Add relationship to Shipment
    shipment = db.relationship('Shipment', backref='quote_request', uselist=False)

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(20), unique=True, nullable=False)
    quote_request_id = db.Column(db.Integer, db.ForeignKey('quote_request.id'))
    
    # Basic Information
    customer_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='Normal')  # High, Medium, Normal
    
    # Pickup Details
    pickup_date = db.Column(db.DateTime)  # When the shipment was picked up
    pickup_time = db.Column(db.String(10))  # Time of pickup (HH:MM format)
    vehicle_plate = db.Column(db.String(20))  # Vehicle plate number that picked up the shipment
    pickup_status = db.Column(db.String(20), default='Pending')  # Pending, Picked Up
    pickup_notes = db.Column(db.Text)  # Any notes about the pickup
    
    # Alternative Contact
    alternative_contact_name = db.Column(db.String(100))
    alternative_contact_phone = db.Column(db.String(20))
    alternative_contact_email = db.Column(db.String(120))
    
    # Locations
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    dropoff_location = db.Column(db.String(200), nullable=False)
    dropoff_lat = db.Column(db.Float)
    dropoff_lng = db.Column(db.Float)
    current_location = db.Column(db.String(200))
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    
    # Cargo Details
    cargo_description = db.Column(db.Text, nullable=False)
    cargo_type = db.Column(db.String(50))  # e.g., Standard, Perishable, Fragile, Hazardous
    weight = db.Column(db.Float)  # in kg
    weight_unit = db.Column(db.String(10), default='kg')
    length = db.Column(db.Float)  # in meters
    width = db.Column(db.Float)   # in meters
    height = db.Column(db.Float)  # in meters
    dimension_unit = db.Column(db.String(10), default='m')
    volume = db.Column(db.Float)  # in cubic meters
    special_handling = db.Column(db.Text)  # Special handling requirements
    
    # Shipping Details
    status = db.Column(db.String(20), default='Pending')  # Pending, In Transit, Delivered
    transport_method = db.Column(db.String(50))  # e.g., Road, Air, Sea, Rail
    estimated_delivery = db.Column(db.DateTime)
    actual_delivery = db.Column(db.DateTime)
    delivery_window_start = db.Column(db.DateTime)  # Preferred delivery window
    delivery_window_end = db.Column(db.DateTime)
    
    # Cost and Insurance
    cost = db.Column(db.Float)  # Total cost
    currency = db.Column(db.String(10), default='USD')
    is_insured = db.Column(db.Boolean, default=False)
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    insurance_coverage_amount = db.Column(db.Float)
    
    # Additional Information
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)  # Notes visible only to admin
    tags = db.Column(db.String(200))  # Comma-separated tags for easy filtering
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Shipment, self).__init__(**kwargs)
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()

    @staticmethod
    def generate_tracking_id():
        # Generate a unique tracking ID with SEG prefix (Segecha)
        return f"SEG{uuid.uuid4().hex[:8].upper()}"
    
    @property
    def dimensions(self):
        """Return formatted dimensions string if available"""
        if self.length and self.width and self.height:
            return f"{self.length}x{self.width}x{self.height} {self.dimension_unit}"
        return None
    
    @property
    def formatted_weight(self):
        """Return formatted weight string if available"""
        if self.weight:
            return f"{self.weight} {self.weight_unit}"
        return None
    
    @property
    def formatted_cost(self):
        """Return formatted cost string if available"""
        if self.cost:
            return f"{self.cost} {self.currency}"
        return None
    
    @property
    def alternative_contact(self):
        """Return formatted alternative contact string if available"""
        if self.alternative_contact_name:
            parts = [self.alternative_contact_name]
            if self.alternative_contact_phone:
                parts.append(self.alternative_contact_phone)
            if self.alternative_contact_email:
                parts.append(self.alternative_contact_email)
            return " | ".join(parts)
        return None

def init_db(app):
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!") 