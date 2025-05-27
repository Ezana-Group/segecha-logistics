import os
from PIL import Image
import glob

def optimize_images(input_dir, output_dir, quality=70):
    """
    Optimize images and convert them to WebP format.
    
    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory to save optimized images
        quality (int): WebP quality (0-100)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files
    image_files = glob.glob(os.path.join(input_dir, '*.jpg')) + \
                 glob.glob(os.path.join(input_dir, '*.jpeg')) + \
                 glob.glob(os.path.join(input_dir, '*.png'))
    
    for img_path in image_files:
        try:
            # Open image
            with Image.open(img_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Generate output filename
                filename = os.path.basename(img_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}.webp")
                
                # Save as WebP
                img.save(output_path, 'WEBP', quality=quality, optimize=True)
                
                print(f"Optimized: {filename} -> {os.path.basename(output_path)}")
                
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")

if __name__ == "__main__":
    # Define directories
    input_dir = "static/images"
    output_dir = "static/images/optimized"
    
    # Run optimization
    optimize_images(input_dir, output_dir) 