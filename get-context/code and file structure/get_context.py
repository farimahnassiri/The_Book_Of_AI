"""
Script Name: get_context.py
Description: This script scans a project's directory, retrieves the file structure, and extracts contents of relevant files. 
             It then generates a structured report (`GET_CONTEXT.txt`) containing the directory tree and file contents. 
             The script excludes unnecessary files and directories such as `node_modules`, `.git`, and certain config files.
Author: Farimah M. Nassiri
Last_Updated: Feb 19, 2025. 
Version: 2.0
"""
import os

def get_file_structure(root_dir):
    file_structure = []
    files_content = []
    
    # Define allowed file extensions
    allowed_extensions = ('.ts', '.tsx', '.js', '.jsx', '.css', '.scss', '.html', '.json', '.md', '.txt', '.mjs')
    
    # Define directories to skip
    skip_dirs = {'node_modules', 'public', '.git', '.next', '.vercel'}
    
    # Define files to skip entirely - will not even attempt to open these
    skip_files = {'.DS_Store', '.gitignore', 'package-lock.json', 'yarn.lock', '.env.local', 'README.md', '.env'}
    
    for subdir, dirs, files in os.walk(root_dir):
        # Skip unwanted directories immediately
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            # Skip files that match any patterns we want to ignore
            if (file in skip_files or 
                file.endswith('.env.local') or  # Additional check for .env.local
                os.path.basename(file) in skip_files):
                continue
            
            file_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(file_path, root_dir)
            
            # Check if file extension is allowed or if it's a specific file we want
            if (file.lower().endswith(allowed_extensions) or 
                file in {'package.json', 'tsconfig.json'}):
                try:
                    # Add to file structure
                    file_structure.append(relative_path)
                    
                    # Read and add content for text files
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                        files_content.append((relative_path, file_content))
                        
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
    
    return file_structure, files_content

def write_context_file(file_structure, files_content, output_file):
    total_files = len(file_structure)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("===================================================================\n")
        f.write("                   FILES & FOLDER STRUCTURE\n")
        f.write("===================================================================\n\n")
        
        # Create tree structure
        tree = {}
        for path in sorted(file_structure):
            parts = path.split(os.sep)
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        # Write tree structure
        def write_tree(level, indent=""):
            for name, subtree in sorted(level.items()):
                if subtree:
                    f.write(f"{indent}+ {name}/\n")
                    write_tree(subtree, indent + "  ")
                else:
                    f.write(f"{indent}  - {name}\n")
        
        write_tree(tree)
        
        # Write file count
        f.write(f"\n===== TOTAL FILES: {total_files} =====\n\n")
        
        # Write file contents
        for path, content in sorted(files_content):
            f.write("===================================================================\n")
            f.write(f"FILE PATH: {os.path.join(path)}\n")
            f.write("===================================================================\n\n")
            f.write(content)
            f.write("\n// END OF FILE\n\n")

def main():
    root_dir = '.'  # Current directory
    output_file = 'GET_CONTEXT.txt'
    
    try:
        file_structure, files_content = get_file_structure(root_dir)
        write_context_file(file_structure, files_content, output_file)
        print(f"Context file '{output_file}' created successfully!")
        print(f"Total files processed: {len(file_structure)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()