import os
import subprocess

def build_css():
    """Build Tailwind CSS file."""
    try:
        # Create css directory if it doesn't exist
        os.makedirs('static/css', exist_ok=True)
        
        # Run Tailwind CLI to build CSS
        subprocess.run([
            'npx',
            'tailwindcss',
            '-i',
            'static/css/input.css',
            '-o',
            'static/css/tailwind.css',
            '--minify'
        ], check=True)
        
        print("Successfully built Tailwind CSS")
    except subprocess.CalledProcessError as e:
        print(f"Error building CSS: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    build_css() 