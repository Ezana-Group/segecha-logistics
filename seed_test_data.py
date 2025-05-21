import os
from datetime import datetime, timedelta, date
from app import app, db
from database import Admin, Shipment, QuoteRequest
from werkzeug.security import generate_password_hash

with app.app_context():
    # 1. Add test admin
    admin_email = 'testadmin@segecha.com'
    admin = Admin.query.filter_by(email=admin_email).first()
    if not admin:
        admin = Admin(email=admin_email)
        admin.set_password('testpassword123')
        db.session.add(admin)
        print(f"Added test admin: {admin_email}")
    else:
        print(f"Test admin already exists: {admin_email}")

    # 2. Add test shipments
    for i in range(1, 6):
        tracking_id = f"SEGTEST{i:04d}"
        shipment = Shipment.query.filter_by(tracking_id=tracking_id).first()
        if not shipment:
            shipment = Shipment(
                tracking_id=tracking_id,
                customer_name=f"Test Customer {i}",
                priority='High' if i % 2 == 0 else 'Normal',
                pickup_date=datetime.utcnow() - timedelta(days=i),
                pickup_time="09:00",
                vehicle_plate=f"KDA 12{i}A",
                pickup_status='Picked Up',
                pickup_notes=f"Pickup note {i}",
                alternative_contact_name=f"Alt Contact {i}",
                alternative_contact_phone=f"+2547000000{i}",
                alternative_contact_email=f"alt{i}@test.com",
                pickup_location="Nairobi, Kenya",
                pickup_lat=-1.2921,
                pickup_lng=36.8219,
                dropoff_location="Mombasa, Kenya",
                dropoff_lat=-4.0435,
                dropoff_lng=39.6682,
                current_location="Mombasa, Kenya",
                current_lat=-4.0435,
                current_lng=39.6682,
                cargo_description=f"Test cargo {i}",
                cargo_type="Standard",
                weight=1000 + i * 100,
                weight_unit="kg",
                length=2.5,
                width=1.5,
                height=1.2,
                dimension_unit="m",
                volume=4.5,
                special_handling="None",
                status='In Transit' if i % 2 == 0 else 'Pending',
                transport_method='Road',
                estimated_delivery=datetime.utcnow() + timedelta(days=2),
                actual_delivery=None,
                delivery_window_start=datetime.utcnow() + timedelta(days=1),
                delivery_window_end=datetime.utcnow() + timedelta(days=2),
                cost=50000 + i * 5000,
                currency="KES",
                is_insured=True,
                insurance_provider="Test Insurance",
                insurance_policy_number=f"POLICY{i:04d}",
                insurance_coverage_amount=1000000,
                notes=f"Test shipment note {i}",
                internal_notes=f"Internal note {i}",
                tags="test,shipment",
                created_at=datetime.utcnow() - timedelta(days=i),
                updated_at=datetime.utcnow()
            )
            db.session.add(shipment)
            print(f"Added test shipment: {tracking_id}")
        else:
            print(f"Test shipment already exists: {tracking_id}")

    # 3. Add test quote requests
    for i in range(1, 6):
        email = f"testuser{i}@example.com"
        quote = QuoteRequest.query.filter_by(email=email).first()
        if not quote:
            quote = QuoteRequest(
                name=f"Test User {i}",
                company=f"Test Company {i}",
                email=email,
                phone=f"+2547010000{i}",
                pickup_location="Nairobi, Kenya",
                pickup_lat=-1.2921,
                pickup_lng=36.8219,
                dropoff_location="Mombasa, Kenya",
                dropoff_lat=-4.0435,
                dropoff_lng=39.6682,
                estimated_distance=480.0,
                cargo_description=f"Test cargo description {i}",
                preferred_date=date.today() + timedelta(days=i),
                additional_notes=f"Test additional notes {i}",
                created_at=datetime.utcnow() - timedelta(days=i),
                reviewed=(i % 2 == 0)
            )
            db.session.add(quote)
            print(f"Added test quote request: {email}")
        else:
            print(f"Test quote request already exists: {email}")

    db.session.commit()
    print("Test data inserted successfully.") 