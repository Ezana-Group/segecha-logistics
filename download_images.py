import os
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

# Create images directory if it doesn't exist
IMAGES_DIR = 'static/images'
os.makedirs(IMAGES_DIR, exist_ok=True)

# Dictionary mapping file names to search queries and descriptions
IMAGE_CONFIGS = {
    'hero_mercedes_actros.jpg': {
        'query': 'mercedes actros truck highway africa sunset',
        'url': 'https://images.unsplash.com/photo-1519003722824-194d4455a60c'
    },
    'african_team.jpg': {
        'query': 'logistics team africa office',
        'url': 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0'
    },
    'long_haul_fleet.jpg': {
        'query': 'truck fleet highway transport',
        'url': 'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7'
    },
    'fleet_tracking_room.jpg': {
        'query': 'logistics control room dispatch',
        'url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40'
    },
    'tracking_map.jpg': {
        'query': 'africa map logistics route',
        'url': 'https://images.unsplash.com/photo-1524661135-423995f22d0b'
    },
    'quote_officer.jpg': {
        'query': 'logistics manager office professional',
        'url': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e'
    },
    'office_contact.jpg': {
        'query': 'modern office building corporate',
        'url': 'https://images.unsplash.com/photo-1497366216548-37526070297c'
    }
}

def download_and_save_image(url, filename):
    try:
        # Download image
        response = requests.get(url)
        response.raise_for_status()
        
        # Open and process image
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary (in case of PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Save image with quality optimization
        filepath = os.path.join(IMAGES_DIR, filename)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        print(f"✅ Successfully downloaded: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ Error downloading {filename}: {str(e)}")
        return False

def main():
    print("🚀 Starting image downloads...")
    
    success_count = 0
    for filename, config in IMAGE_CONFIGS.items():
        print(f"\n📥 Downloading {filename}...")
        if download_and_save_image(config['url'], filename):
            success_count += 1
    
    print(f"\n✨ Download complete! Successfully downloaded {success_count}/{len(IMAGE_CONFIGS)} images.")

if __name__ == "__main__":
    main() 