import click
from flask.cli import with_appcontext
from database import db, Admin

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    
    # Create admin user
    admin = Admin(email='admin@segecha.com')
    admin.set_password('admin123')  # Change this in production
    db.session.add(admin)
    
    try:
        db.session.commit()
        click.echo('Initialized the database and created admin user.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error initializing database: {e}', err=True) 