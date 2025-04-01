"""
Script Name: pi_digit_formatter.py
Description: This script calculates and formats pi to a user-specified number of decimal places.
 It allows for customized display options including space-separated digits, 
 line-by-line formatting with custom digits per line, or custom separators between
 digits. The formatted output can be viewed in the console and optionally saved
 to a text file.

Dependencies:
- mpmath (arbitrary precision arithmetic library)
- textwrap (text wrapping and filling library from standard library)

Installation:
Make sure you have mpmath installed. You can install it using:
 pip install mpmath

How to Use:
1. Run the script with Python 3.12.2:
   python pi_digit_formatter.py
2. Enter the number of decimal places when prompted.
3. Choose a formatting option (spaces, newlines, or custom separator).
4. Optionally save the output to a file.

Notes:
- Large numbers of digits (>10,000) may take longer to process.
- The script implements memory-efficient handling of large digit sequences.

Author: Farimah M. Nassiri
Date: 2025-04-01
Version: 1.0
"""

import mpmath
import textwrap
import sys
import os
from time import time


def get_pi_digits(num_digits):
    """
    Get pi to specified number of decimal places.
    
    Args:
        num_digits (int): Number of decimal places to calculate
        
    Returns:
        str: String of pi decimal digits (without the "3.")
        
    Raises:
        ValueError: If num_digits is not a positive integer
        Exception: For other calculation errors
    """
    if not isinstance(num_digits, int):
        raise ValueError("Number of digits must be an integer")
    if num_digits < 2:
        raise ValueError("Number of digits must be at least 2")
        
    try:
        mpmath.mp.dps = num_digits + 10  
        pi_str = str(mpmath.mp.pi)
        pi_decimal = pi_str[2:2+num_digits]
        return pi_decimal
    except Exception as e:
        raise Exception(f"Error calculating pi: {str(e)}")


def format_pi_with_spaces(pi_decimal):
    """
    Format pi decimal digits with spaces between each digit.
    
    Args:
        pi_decimal (str): String of pi decimal digits
        
    Returns:
        str: Formatted string with spaces between digits
    """
    return "3 . " + " ".join(pi_decimal)


def format_pi_with_newlines(pi_decimal, digits_per_line=50):
    """
    Format pi decimal digits with aligned newlines.
    
    Args:
        pi_decimal (str): String of pi decimal digits
        digits_per_line (int, optional): Number of digits per line. Defaults to 50.
        
    Returns:
        str: Formatted string with digits broken into aligned lines
    """
    chunks = textwrap.wrap(pi_decimal, digits_per_line)
    
    formatted_lines = ["3." + chunks[0]]
    
    for chunk in chunks[1:]:
        formatted_lines.append("  " + chunk)
    
    return "\n".join(formatted_lines)


def format_pi_with_custom_separator(pi_decimal, separator):
    """
    Format pi decimal digits with a custom separator.
    
    Args:
        pi_decimal (str): String of pi decimal digits
        separator (str): Custom separator to place between digits
        
    Returns:
        str: Formatted string with custom separators between digits
    """
    return "3." + separator.join(pi_decimal)


def get_integer_input(prompt, min_value=None, max_value=None, warning_threshold=None, warning_message=None, max_attempts=3):
    """
    Get an integer input from the user with validation.
    
    Args:
        prompt (str): Prompt to display to the user
        min_value (int, optional): Minimum acceptable value
        max_value (int, optional): Maximum acceptable value
        warning_threshold (int, optional): Value that triggers a warning
        warning_message (str, optional): Warning message to display
        max_attempts (int, optional): Maximum number of incorrect attempts before terminating
        
    Returns:
        int: Valid integer input from the user
        
    Raises:
        SystemExit: If maximum number of attempts is exceeded
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            value = input(prompt).strip()
            if not value:
                print("Please enter a value.")
                attempts += 1
                if attempts >= max_attempts:
                    print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                    sys.exit(1)
                continue
            
            # Check if the input is a valid integer
            try:
                value = int(value)
            except ValueError:
                print("Please enter a valid integer number.")
                attempts += 1
                if attempts >= max_attempts:
                    print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                    sys.exit(1)
                continue
                
            # Validate minimum value
            if min_value is not None and value < min_value:
                print(f"Please enter a value greater than or equal to {min_value}.")
                attempts += 1
                if attempts >= max_attempts:
                    print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                    sys.exit(1)
                continue
                
            # Validate maximum value
            if max_value is not None and value > max_value:
                print(f"Please enter a value less than or equal to {max_value}.")
                attempts += 1
                if attempts >= max_attempts:
                    print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                    sys.exit(1)
                continue
                
            # Handle warning threshold
            if warning_threshold is not None and value > warning_threshold:
                print(warning_message)
                while True:
                    confirm = input("Continue? (y/n): ").lower().strip()
                    if confirm in ['y', 'yes']:
                        break
                    elif confirm in ['n', 'no']:
                        print("Please enter a smaller value.")
                        # We don't count this as a failed attempt
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                
                if confirm in ['n', 'no']:
                    continue
                    
            return value
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}. Please try again.")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)


def get_option_input(prompt, options, max_attempts=3):
    """
    Get an option input from the user with validation.
    
    Args:
        prompt (str): Prompt to display to the user
        options (list or dict): Valid options
        max_attempts (int, optional): Maximum number of incorrect attempts before terminating
        
    Returns:
        Any: Selected option from the user
        
    Raises:
        SystemExit: If maximum number of attempts is exceeded
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            value = input(prompt)
            if not value.strip():
                print("Please enter a value.")
                attempts += 1
                if attempts >= max_attempts:
                    print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                    sys.exit(1)
                continue
                
            if isinstance(options, dict):
                if value in options:
                    return value
                valid_options = ", ".join(str(opt) for opt in options.keys())
            else:
                if value in options:
                    return value
                valid_options = ", ".join(str(opt) for opt in options)
                
            print(f"Please enter a valid option from: {valid_options}")
            attempts += 1
            
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}. Please try again.")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)


def save_to_file(content, default_filename="pi_digits.txt", max_attempts=3):
    """
    Save content to a file with error handling.
    
    Args:
        content (str): Content to save
        default_filename (str, optional): Default filename. Defaults to "pi_digits.txt".
        max_attempts (int, optional): Maximum number of incorrect attempts before terminating
        
    Returns:
        bool: True if save was successful, False otherwise
        
    Raises:
        SystemExit: If maximum number of attempts is exceeded
    """
    attempts = 0
    while attempts < max_attempts:
        filename = input(f"Enter filename (default: {default_filename}): ").strip() or default_filename
        
        # Validate filename
        if not filename:
            print("Filename cannot be empty.")
            attempts += 1
            continue
        
        # Add .txt extension if no extension was provided
        if '.' not in filename:
            filename += '.txt'
            
        try:
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except PermissionError:
                    print(f"Permission denied: Cannot create directory '{directory}'.")
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                        sys.exit(1)
                    continue
                except Exception as e:
                    print(f"Error creating directory: {str(e)}")
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                        sys.exit(1)
                    continue
            
            # Check if file exists and confirm overwrite
            if os.path.exists(filename):
                confirm = input(f"File '{filename}' already exists. Overwrite? (y/n): ").lower()
                if confirm not in ['y', 'yes']:
                    attempts += 1
                    continue
                    
            with open(filename, 'w') as f:
                f.write(content)
            print(f"File saved successfully to {os.path.abspath(filename)}")
            return True
            
        except PermissionError:
            print(f"Permission denied: Cannot write to file '{filename}'.")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)
        except IOError as e:
            print(f"Error saving file: {str(e)}")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error saving file: {str(e)}")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts ({max_attempts}) exceeded. Terminating program.")
                sys.exit(1)
    
    return False


def print_progress(message):
    """Print a progress message with timestamp."""
    print(f"[{time():.2f}s] {message}")


def main():
    """Main function to run the Pi Digit Formatter program."""
    print("\n" + "="*50)
    print("Pi Digit Formatter".center(50))
    print("="*50 + "\n")
    print("Recommended Python version: 3.12.2\n")
    
    try:
        # Define memory and time limits based on system capabilities
        MAX_RECOMMENDED_DIGITS = 100000
        VERY_LARGE_THRESHOLD = 10000
        
        num_digits = get_integer_input(
            "How many decimal places of pi would you like? ",
            min_value=2,  # Enforcing minimum of 2 digits
            warning_threshold=VERY_LARGE_THRESHOLD,
            warning_message=f"Warning: Calculating {VERY_LARGE_THRESHOLD}+ digits may take significant time and memory."
        )
        
        # Additional warning for extremely large calculations
        if num_digits > MAX_RECOMMENDED_DIGITS:
            print(f"\nCAUTION: Calculating {num_digits:,} digits may cause system instability.")
            confirm = get_option_input("Are you sure you want to continue? (y/n): ", ["y", "n", "yes", "no"])
            if confirm.lower() not in ["y", "yes"]:
                print("Operation cancelled. Please try with a smaller number.")
                sys.exit(0)
        
        print_progress(f"Calculating pi to {num_digits:,} decimal places...")
        start_time = time()
        
        try:
            pi_decimal = get_pi_digits(num_digits)
            calc_time = time() - start_time
            print_progress(f"Calculation completed in {calc_time:.2f} seconds")
            
            # Performance metrics
            if calc_time > 5:
                digits_per_second = num_digits / calc_time
                print(f"Performance: {digits_per_second:.2f} digits per second")
        except MemoryError:
            print("\nERROR: Not enough memory to calculate this many digits.")
            print("Please try again with a smaller number of digits.")
            sys.exit(1)
        except Exception as e:
            print(f"\nERROR during calculation: {str(e)}")
            sys.exit(1)
        
        print("\nHow would you like the digits to be formatted?")
        print("1. Separated by spaces")
        print("2. Separated by newlines")
        print("3. Separated by a custom character")
        
        format_options = {"1": "spaces", "2": "newlines", "3": "custom"}
        choice = get_option_input("Enter your choice (1-3): ", format_options)
        
        if choice == "1":
            formatted_pi = format_pi_with_spaces(pi_decimal)
        elif choice == "2":
            # Get digits per line with default of 50 if user just presses Enter
            default_line_length = min(50, num_digits)
            digits_per_line = None
            
            while digits_per_line is None:
                digits_per_line_input = input(f"How many digits per line? (default {default_line_length}): ").strip()
                
                if not digits_per_line_input:
                    digits_per_line = default_line_length
                else:
                    try:
                        digits_per_line = int(digits_per_line_input)
                        if digits_per_line < 1:
                            print("Number of digits per line must be at least 1.")
                            digits_per_line = None
                        elif digits_per_line > num_digits:
                            print(f"Number of digits per line cannot exceed total digits ({num_digits}).")
                            digits_per_line = None
                    except ValueError:
                        print("Please enter a valid integer.")
                        digits_per_line = None
            
            formatted_pi = format_pi_with_newlines(pi_decimal, digits_per_line)
        elif choice == "3":
            # Handle empty separator input
            separator = ""
            attempts = 0
            while not separator and attempts < 3:
                separator = input("Enter custom separator: ")
                if not separator:
                    print("Separator cannot be empty. Please enter a valid separator.")
                    attempts += 1
                    if attempts >= 3:
                        print("Maximum number of attempts (3) exceeded. Using default separator ','.")
                        separator = ","
            formatted_pi = format_pi_with_custom_separator(pi_decimal, separator)
            
        # Calculate output size
        output_size_bytes = len(formatted_pi.encode('utf-8'))
        output_size_mb = output_size_bytes / (1024 * 1024)
        
        # Print preview
        preview_length = min(100, len(formatted_pi))
        print(f"\nPreview of formatted pi (first {preview_length} characters):")
        print(formatted_pi[:preview_length] + ("..." if len(formatted_pi) > preview_length else ""))
        
        # Show output stats
        print(f"\nOutput size: {output_size_bytes:,} bytes", end="")
        if output_size_mb >= 1:
            print(f" ({output_size_mb:.2f} MB)")
        else:
            print("")
        
        # Ask if user wants to save to file
        save_choice = get_option_input("Save to file? (y/n): ", ["y", "n", "yes", "no"])
        if save_choice.lower() in ["y", "yes"]:
            save_to_file(formatted_pi)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except MemoryError:
        print("\nError: Not enough memory to complete the operation.")
        print("Try with a smaller number of digits.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)
        
    print("\nEnjoy your slice of the π! 🥧")


if __name__ == "__main__":
    main()