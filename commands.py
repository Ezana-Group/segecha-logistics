import click
from flask.cli import with_appcontext
from database import db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    
    try:
        db.session.commit()
        click.echo('Initialized the database.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error initializing database: {e}', err=True) 