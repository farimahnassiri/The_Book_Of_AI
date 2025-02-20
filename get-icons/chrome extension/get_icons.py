"""
Script Name: chrome_extension_icon_generator.py
Description: This script automatically generates Chrome Extension icons in various sizes 
             by resizing supported image formats (PNG, JPG, JPEG, SVG, WEBP, GIF). 
             The script saves the icons in a uniquely named folder and provides a 
             ready-to-use JSON snippet for the Chrome Extension manifest file.

Dependencies:
- Pillow (Python Imaging Library fork for image processing)

Installation:
Make sure you have Pillow installed. You can install it using:
    pip install Pillow

How to Use:
1. Place your image files in the same directory as this script.
2. Run the script:
    python chrome_extension_icon_generator.py
3. Enter a prefix for the icon filenames when prompted (or press Enter to use the default prefix 'icon').
4. Copy the generated JSON snippet into your Chrome Extension's manifest.json file under the 'icons' key.

Author: Farimah M. Nassiri
Date: 2025-02-19
Version: 1.0
"""

from PIL import Image
import os
import json

# Define required sizes for Chrome Extension icons
sizes = [16, 32, 48, 128, 256, 512]
supported_formats = ['.png', '.jpg', '.jpeg', '.svg', '.webp', '.gif']

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Change working directory to script's location

# Find all image files in the script's directory
def find_image_files():
    """Returns a list of image files in the current directory with supported formats."""
    return [file for file in os.listdir(script_dir) if os.path.splitext(file)[1].lower() in supported_formats]

# Determine the next available folder name for storing icons
def get_next_icon_folder():
    """Generates a unique folder name for each batch of icons."""
    base_folder = "icons"
    counter = 0
    
    while True:
        folder_name = f"{base_folder}-{counter}" if counter > 0 else base_folder
        folder_path = os.path.join(script_dir, folder_name)
        if not os.path.exists(folder_path):
            return folder_path
        counter += 1

# Load and process each image
def generate_icons_for_images(image_files, icon_prefix, output_dir):
    """Generates icons for each found image and returns a list for Chrome manifest."""
    manifest_icons = {}
    
    os.makedirs(output_dir, exist_ok=True)

    for image_filename in image_files:
        image_path = os.path.join(script_dir, image_filename)
        
        try:
            # Open image
            img = Image.open(image_path)

            # Generate resized icons
            for size in sizes:
                output_filename = f"{icon_prefix}-{size}.png"
                output_file = os.path.join(output_dir, output_filename)
                
                resized_img = img.resize((size, size), Image.LANCZOS)
                resized_img.save(output_file, format="PNG")
                
                # Add to manifest format
                manifest_icons[str(size)] = os.path.join(os.path.basename(output_dir), output_filename)

        except Exception as e:
            print(f"❌ Error processing {image_filename}: {e}")

    return manifest_icons

def main():
    image_files = find_image_files()

    if image_files:
        print(f"Found {len(image_files)} image(s): {', '.join(image_files)}\n")

        # Ask user for a custom icon name prefix or use default
        icon_prefix = input("Enter a prefix for the icon filenames (default is 'icon'): ").strip() or "icon"
        
        # Get the next available folder for icons
        output_dir = get_next_icon_folder()

        manifest_icons = generate_icons_for_images(image_files, icon_prefix, output_dir)

        print(f"\n🎉 Icons successfully resized and saved in '{output_dir}' folder!")
        
        # Format and display the manifest.json content in a copy-paste friendly way
        print("\n📄 Chrome Extension Manifest Icons Format (Copy & Paste):\n")
        print(json.dumps(manifest_icons, indent=4))
        print("\n✅ Copy the above JSON snippet into your manifest.json file under the 'icons' key.")
        
    else:
        print("❌ No supported image files found in the current directory.")

if __name__ == "__main__":
    main()
