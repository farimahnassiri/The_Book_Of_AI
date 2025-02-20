"""
Script Name: svg_context.py
Description: This script automatically processes the first SVG file found in the same directory,
             extracts its elements and attributes, and generates a formatted output in 'svg-styling.text'. 
             The script also sanitizes 'path' elements by replacing the 'd' attribute 
             with a placeholder ('--some-arbitrary-path') for security or styling purposes.

Dependencies:
- Standard Python Library (no external packages required)

Installation:
No additional installation is required. This script only uses standard Python libraries.

How to Use:
1. Place your SVG file in the same directory as this script.
2. Run the script:
    python svg_context.py
3. The output will be saved to 'svg-styling.text' in the same directory.

Author: Farimah M. Nassiri
Date: 2025-02-19
Version: 2.0
"""

import xml.etree.ElementTree as ET
import os
import glob

def process_svg(svg_file):
    if not os.path.isfile(svg_file):
        print(f"Error: The file '{svg_file}' does not exist.")
        return

    try:
        relative_path = os.path.relpath(svg_file)
        tree = ET.parse(svg_file)
        root = tree.getroot()
        
        with open('svg-styling.text', 'w') as f:
            f.write(f"SVG File: {relative_path}\n\n")
            
            def process_element(element, level=0):
                tag = element.tag.split('}')[-1]
                attrs = element.attrib.copy()

                if tag == 'path' and 'd' in attrs:
                    attrs['d'] = '--some-arbitrary-path'
                
                attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
                f.write('  ' * level + f"<{tag} {attr_str}>\n")
                
                for child in element:
                    process_element(child, level + 1)
                
                f.write('  ' * level + f"</{tag}>\n")
            
            process_element(root)
        
        print(f"🎉 Processing complete. Output written to 'svg-styling.text'")
    
    except ET.ParseError:
        print(f"❌ Error: Unable to parse '{svg_file}'. Make sure it's a valid SVG file.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    svg_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.svg"))
    
    if not svg_files:
        print("❌ No SVG files found in the current directory. Please add an SVG file and try again.")
        return
    
    svg_file = svg_files[0]  # Automatically select the first SVG file found
    print(f"🚀 Found SVG file: {svg_file}")
    process_svg(svg_file)

if __name__ == "__main__":
    main()
