import os
from PIL import Image
import glob

def optimize_image(input_path, output_path, max_width=None, max_height=None, quality=85):
    """Optimize and resize an image."""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            if max_width or max_height:
                width, height = img.size
                if max_width and width > max_width:
                    ratio = max_width / width
                    height = int(height * ratio)
                    width = max_width
                if max_height and height > max_height:
                    ratio = max_height / height
                    width = int(width * ratio)
                    height = max_height
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save as WebP
            img.save(output_path, 'WEBP', quality=quality, method=6)
            print(f"Optimized: {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def main():
    # Create optimized directory if it doesn't exist
    optimized_dir = os.path.join('static', 'images', 'optimized')
    os.makedirs(optimized_dir, exist_ok=True)
    
    # Image size configurations
    image_sizes = {
        'hero_mercedes_actros': (1920, 1080),
        'hero_truck': (800, 600),
        'fleet_tracking_room': (800, 600),
        'tracking_page_map': (800, 600),
        'fleet_africa': (800, 600),
        'team_dispatch': (800, 600),
        'border_checkpoint': (800, 600),
        'warehouse_loading': (800, 600),
        'gps_tracking_map': (800, 600),
        'logo-main': (144, 48),
        'logo-sg-group': (160, 32),
        'logo-sg': (40, 40),
        'logo-icon': (40, 40)
    }
    
    # Process all images in the static/images directory
    image_dir = os.path.join('static', 'images')
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        for img_path in glob.glob(os.path.join(image_dir, ext)):
            filename = os.path.basename(img_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # Get size configuration if available
            max_width, max_height = image_sizes.get(name_without_ext, (None, None))
            
            # Create WebP version
            webp_path = os.path.join(optimized_dir, f"{name_without_ext}.webp")
            optimize_image(img_path, webp_path, max_width, max_height)

if __name__ == '__main__':
    main() 