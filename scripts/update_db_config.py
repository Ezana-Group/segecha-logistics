import os
from pathlib import Path

def update_db_config():
    """Update database configuration in .env file."""
    env_path = Path('.env')
    if not env_path.exists():
        print("Error: .env file not found")
        return
    
    # Read current .env file
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update database URL
    new_lines = []
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append('DATABASE_URL=postgresql://localhost:5432/segecha_logistics\n')
        else:
            new_lines.append(line)
    
    # Write updated content
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    
    print("Updated database configuration in .env file")

if __name__ == '__main__':
    update_db_config() 