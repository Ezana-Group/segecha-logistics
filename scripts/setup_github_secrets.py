import os
import secrets
import string
import subprocess
from pathlib import Path

def generate_ssh_key():
    """Generate SSH key for deployment."""
    key_path = Path.home() / '.ssh' / 'segecha_deploy'
    
    if not key_path.exists():
        # Generate SSH key
        subprocess.run([
            'ssh-keygen',
            '-t', 'ed25519',
            '-f', str(key_path),
            '-N', '',
            '-C', 'segecha-deploy-key'
        ], check=True)
    
    # Read public key
    with open(f"{key_path}.pub", 'r') as f:
        public_key = f.read().strip()
    
    return public_key

def setup_github_secrets():
    """Set up GitHub repository secrets for CI/CD."""
    print("Setting up GitHub repository secrets...")
    print("\nPlease run the following commands in your GitHub repository settings:")
    print("\n1. Go to Settings > Secrets and variables > Actions")
    print("2. Add the following secrets:")
    
    # Generate deployment key
    deploy_key = generate_ssh_key()
    print(f"\nDEPLOY_KEY:\n{deploy_key}")
    
    # Other required secrets
    secrets_to_add = {
        'HOST': 'your-server-hostname',
        'USERNAME': 'your-server-username',
        'DATABASE_URL': 'your-production-database-url',
        'SECRET_KEY': ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)),
        'JWT_SECRET_KEY': ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)),
        'SMTP_USERNAME': 'your-smtp-username',
        'SMTP_PASSWORD': 'your-smtp-password',
        'MPESA_CONSUMER_KEY': 'your-mpesa-consumer-key',
        'MPESA_CONSUMER_SECRET': 'your-mpesa-consumer-secret',
        'MPESA_PASSKEY': 'your-mpesa-passkey',
        'MPESA_SHORTCODE': 'your-mpesa-shortcode',
        'GOOGLE_MAPS_API_KEY': 'your-google-maps-api-key',
        'OPENCAGE_API_KEY': 'your-opencage-api-key',
        'SMS_API_KEY': 'your-sms-api-key'
    }
    
    print("\nOther required secrets:")
    for key, value in secrets_to_add.items():
        print(f"\n{key}: {value}")
    
    print("\nAfter adding these secrets, your CI/CD pipeline will be able to deploy to your server.")

if __name__ == '__main__':
    setup_github_secrets() 