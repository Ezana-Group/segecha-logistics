import os
import shutil
from datetime import datetime
import subprocess
from pathlib import Path

def create_backup():
    """Create a backup of the database and important files."""
    # Create backup directory if it doesn't exist
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'backup_{timestamp}'
    backup_path = backup_dir / backup_name
    
    # Create backup directory
    backup_path.mkdir(exist_ok=True)
    
    # Backup database
    try:
        # Assuming PostgreSQL database
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            db_backup_file = backup_path / 'database.sql'
            subprocess.run([
                'pg_dump',
                db_url,
                '-f', str(db_backup_file)
            ], check=True)
    except Exception as e:
        print(f"Error backing up database: {e}")
    
    # Backup important files
    important_files = [
        'config.py',
        'requirements.txt',
        '.env'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            shutil.copy2(file, backup_path / file)
    
    # Backup uploads directory if it exists
    uploads_dir = Path('uploads')
    if uploads_dir.exists():
        shutil.copytree(uploads_dir, backup_path / 'uploads')
    
    # Create zip archive
    shutil.make_archive(str(backup_path), 'zip', backup_path)
    
    # Remove the unzipped backup directory
    shutil.rmtree(backup_path)
    
    # Clean up old backups (keep last 30 days)
    cleanup_old_backups()
    
    print(f"Backup created successfully: {backup_path}.zip")

def cleanup_old_backups():
    """Remove backups older than 30 days."""
    backup_dir = Path('backups')
    current_time = datetime.now()
    
    for backup_file in backup_dir.glob('backup_*.zip'):
        file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
        age_days = (current_time - file_time).days
        
        if age_days > 30:
            backup_file.unlink()
            print(f"Removed old backup: {backup_file}")

if __name__ == '__main__':
    create_backup() 