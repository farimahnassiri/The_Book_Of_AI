import os
from bs4 import BeautifulSoup

def find_html_file():
    """Search for an HTML file in the current directory."""
    for file in os.listdir('.'):
        if file.endswith('.html'):
            return file
    return None

def extract_text_from_html(input_file):
    """Extract text from the specified HTML file and save it to a text file."""
    try:
        # Generate output filename
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_GOT_TEXT.txt"

        # Read the input HTML file
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract text content from specific tags (including headers)
        text_content = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.get_text().strip()
            if text:  # Only add non-empty strings
                text_content.append(text)

        # Join the extracted text with newlines
        extracted_text = '\n\n'.join(text_content)

        # Write the extracted text to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(extracted_text)

        print(f"Text extracted from '{input_file}' and saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except IOError as e:
        print(f"Error: An I/O error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # Find the HTML file in the current directory
    input_file = find_html_file()

    if input_file:
        # Run the extraction function
        extract_text_from_html(input_file)
    else:
        print("Error: No HTML file found in the current directory.")

if __name__ == "__main__":
    main()
