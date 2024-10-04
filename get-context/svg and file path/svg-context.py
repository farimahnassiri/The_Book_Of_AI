# Replace './_FILE_PATH_NAME' with your svg file name

import xml.etree.ElementTree as ET
import os

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

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
        
        print(f"Processing complete. Output written to 'svg-styling.text'")
    
    except ET.ParseError:
        print(f"Error: Unable to parse '{svg_file}'. Make sure it's a valid SVG file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage
svg_file = os.path.join(os.getcwd(), './_FILE_PATH_NAME')
print(f"Attempting to process file: {svg_file}")
process_svg(svg_file)