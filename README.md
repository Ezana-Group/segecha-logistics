# Segecha Logistics Platform

A comprehensive logistics and shipment tracking platform built for Segecha Group Ltd.

## Features

### Quote Request System
- Multi-step quote request form with validation
- Location selection with map integration
- Cargo details and personal information collection
- Real-time validation and error handling

### Shipment Tracking
- Real-time shipment tracking with map visualization
- Route display showing quickest path between pickup and delivery
- Current location tracking with animated markers
- Estimated delivery time and distance calculation
- Status updates and notifications

### Admin Dashboard
- Comprehensive shipment management
- Quote request processing
- Status updates and shipment creation
- Route visualization and management
- Customer information management

## Technical Stack

- Frontend: HTML, TailwindCSS, JavaScript
- Maps: Leaflet.js with OpenStreetMap
- Routing: OSRM (Open Source Routing Machine)
- Backend: Python Flask
- Database: SQLAlchemy

## Map Features

The platform uses advanced mapping features including:
- Interactive maps for location selection
- Real-time route calculation and display
- Distance and time estimation
- Custom markers for pickup, delivery, and current location
- Animated current location marker
- Route information popups

## Development Setup

1. Clone the repository
2. Install dependencies
3. Set up environment variables
4. Run the development server

## Environment Variables

Required environment variables:
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
SMTP_SERVER=your_smtp_server
SMTP_PORT=your_smtp_port
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
```

## Project Structure

```
segecha_logistics/
├── templates/
│   ├── base.html
│   ├── quote.html
│   ├── track.html
│   └── admin/
│       ├── dashboard.html
│       └── shipment_form.html
├── static/
│   ├── css/
│   └── js/
├── app.py
└── models.py
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Local Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd segecha_logistics
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   SECRET_KEY=your-secret-key
   ADMIN_EMAIL=admin@segecha.com
   ADMIN_PASSWORD=your-secure-password
   WHATSAPP_NUMBER=254XXXXXXXXX
   ```

5. Initialize the database:
   ```bash
   flask run
   ```
   The database will be automatically created on first run.

6. Access the website:
   - Main site: http://localhost:5000
   - Admin login: http://localhost:5000/admin/login

## Deployment

### Option 1: Traditional Server

1. Set up a Python environment on your server
2. Install dependencies using `requirements.txt`
3. Set up a production WSGI server (e.g., Gunicorn)
4. Configure Nginx/Apache as a reverse proxy
5. Set up SSL certificate
6. Update environment variables

### Option 2: Platform as a Service (e.g., Render.com)

1. Create a new Web Service on Render
2. Connect your repository
3. Set environment variables in the Render dashboard
4. Deploy

## Directory Structure

```
segecha_logistics/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── database.py         # Database models
├── requirements.txt    # Python dependencies
├── static/
│   ├── css/           # Custom CSS files
│   ├── js/            # JavaScript files
│   └── img/           # Images and icons
└── templates/         # HTML templates
    ├── base.html
    ├── index.html
    ├── about.html
    ├── services.html
    ├── quote.html
    ├── contact.html
    ├── admin_login.html
    └── admin_dashboard.html
```

## Customization

1. Update company information in templates
2. Replace placeholder images in `static/img/`
3. Modify color scheme in Tailwind classes
4. Update contact information and social media links
5. Customize Google Maps embed code
6. Add your WhatsApp business number

## Security

- Admin credentials are stored securely using password hashing
- CSRF protection is enabled
- SQL injection protection through SQLAlchemy
- Secure session handling
- Environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@segecha.com or WhatsApp +254 XXX XXX XXX. 