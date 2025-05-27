import os
import subprocess
from pathlib import Path

def init_project():
    """Initialize the entire project."""
    print("Initializing Segecha Logistics project...")
    
    # Create necessary directories
    directories = [
        'logs',
        'backups',
        'uploads',
        'static/uploads',
        'tests/unit',
        'tests/integration',
        'docs/api',
        'docs/deployment'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Set up environment
    print("\nSetting up environment...")
    subprocess.run(['python', 'scripts/setup_env.py'], check=True)
    
    # Set up database
    print("\nSetting up database...")
    subprocess.run(['python', 'scripts/setup_database.py'], check=True)
    
    # Initialize git repository if not already initialized
    if not Path('.git').exists():
        print("\nInitializing git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    # Set up GitHub secrets
    print("\nSetting up GitHub secrets...")
    subprocess.run(['python', 'scripts/setup_github_secrets.py'], check=True)
    
    print("\nProject initialization complete!")
    print("\nNext steps:")
    print("1. Update the .env file with your actual configuration")
    print("2. Set up your GitHub repository and add the secrets")
    print("3. Run the development server: flask run")
    print("4. Access the application at http://localhost:5000")

if __name__ == '__main__':
    init_project() 