import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def setup_database():
    """Set up PostgreSQL database and user."""
    # Load environment variables
    load_dotenv()
    
    # Get database configuration from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return
    
    # Parse database URL
    # Format: postgresql://username:password@host:port/database
    parts = db_url.replace('postgresql://', '').split('@')
    if len(parts) != 2:
        print("Error: Invalid DATABASE_URL format")
        return
    
    user_pass, host_db = parts
    username, password = user_pass.split(':')
    host_port, database = host_db.split('/')
    
    try:
        # Create database and user
        commands = [
            f"sudo -u postgres psql -c \"CREATE USER {username} WITH PASSWORD '{password}';\"",
            f"sudo -u postgres psql -c \"CREATE DATABASE {database};\"",
            f"sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};\""
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True, check=True)
        
        print(f"Successfully created database '{database}' and user '{username}'")
        
        # Initialize database with Flask-Migrate
        subprocess.run("flask db upgrade", shell=True, check=True)
        print("Successfully initialized database with migrations")
        
    except subprocess.CalledProcessError as e:
        print(f"Error setting up database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    setup_database() 