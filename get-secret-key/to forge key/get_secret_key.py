"""
Script Name: secure_key_generator.py
Description: This script generates various types of secure keys, including random alphanumeric, UUID-based, 
             hexadecimal, SHA-256, Base64, numeric (OTP/PIN), passphrase, and HMAC-SHA256 keys. The generated 
             key is displayed for a user-defined time before being securely erased from memory.

Dependencies:
- No external dependencies (uses Python standard libraries)

Usage:
Simply run the script and choose the type of key you want to generate. You can also specify how long you need
to copy the key before it is wiped from memory.

Author: Farimah M. Nassiri
Date: 2025-03-01
Version: 1.0
"""

import secrets
import string
import base64
import uuid
import os
import time
import sys
import threading
import random
import hmac
import hashlib
import gc

# 1. GENERATE RANDOM ALPHANUMERIC KEY
def generate_random_key(length=32):
    """Generate a secure, random alphanumeric key."""
    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(secrets.choice(characters) for _ in range(length))

# 2. GENERATE UUID-BASED KEY
def generate_uuid_key():
    """Generate a secure, unique UUID-based key."""
    return str(uuid.uuid4()).replace("-", "").upper()

# 3. GENERATE HEXADECIMAL KEY
def generate_hex_key(length=32):
    """Generate a secure hexadecimal key."""
    return secrets.token_hex(length // 2)  # Since 1 hex character = 4 bits, divide by 2 for byte length

# 4. GENERATE SHA-256 HASHED KEY
def generate_sha256_key():
    """Generate a SHA-256 hash key from a random 32-byte value."""
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

# 5. GENERATE BASE64-ENCODED KEY
def generate_base64_key(length=32):
    """Generate a secure Base64-encoded key."""
    return base64.urlsafe_b64encode(secrets.token_bytes(length)).decode("utf-8")

# 6. GENERATE NUMERIC KEY (OTP / PIN)
def generate_numeric_key(length=6):
    """Generate a secure numeric key (OTP or PIN)."""
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))

# Wordlist for passphrase generation
WORDLIST = ["alpha", "beta", "gamma", "lana", "delta", "epsilon", "zebra", "tiger", "moon", "galaxy", "ocean", "archer"]

# 7. GENERATE PASSPHRASE KEY
def generate_passphrase(num_words=4):
    """Generate a secure passphrase using random words."""
    return ' '.join(random.choice(WORDLIST) for _ in range(num_words))

# 8. GENERATE HMAC-SHA256 SECURE KEY
def generate_hmac_key(secret="my_secret"):
    """Generate an HMAC-SHA256 key."""
    return hmac.new(secret.encode(), b"secure_data", hashlib.sha256).hexdigest()

# COUNTDOWN TIMER BEFORE KEY ERASURE
def countdown_timer(seconds):
    """Displays a countdown timer and wipes the key after time runs out."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏳ Time remaining: {remaining} seconds... ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r🚨 Time expired! Key has been destroyed.\n")

# WIPE KEY FROM MEMORY
def wipe_key_from_memory(key_ref):
    """Overwrites the key reference in memory before deletion."""
    key_ref = '*' * len(key_ref)  # Overwrite with junk data
    del key_ref  # Delete variable
    gc.collect()  # Force garbage collection

# MAIN FUNCTION
def main():
    print("\n🔹 Secure Key Generator 🔹")
    print("1. Generate Random Alphanumeric Key")
    print("2. Generate UUID-Based Key")
    print("3. Generate a Secure Hexadecimal Key")
    print("4. Generate a SHA-256 Hashed Key")
    print("5. Generate a Secure Base64 Key")
    print("6. Generate a Secure Numeric Key (OTP or PIN)")
    print("7. Generate a Diceware Passphrase (Human-Readable)")
    print("8. Generate an HMAC-SHA256 Secure Key")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        choice = input("Enter choice (1-8): ").strip()

        if choice.isdigit():  # Ensure input is numeric
            choice = int(choice)
            if 1 <= choice <= 8:
                break  # Valid choice, exit loop
            else:
                print("❌ Invalid choice! Please enter a number between 1 and 8.")
        else:
            print("❌ Invalid input! Please enter a number only.")

        attempts += 1
        remaining_attempts = max_attempts - attempts
        if remaining_attempts > 0:
            print(f"⚠️ You have {remaining_attempts} attempt(s) left.\n")
        else:
            print("🚨 Too many invalid attempts. Exiting!")
            sys.exit(1)  # Exit with an error code

    # Ask user for timer duration first
    try:
        seconds = int(input("⏳ Enter how long you need to copy the key (max 60 seconds, default 20): ") or 20)
        if seconds < 1:
            print("⚠️ Time must be at least 1 second! Defaulting to 20 seconds.")
            seconds = 20
        elif seconds > 60:
            print("⚠️ Maximum allowed time is 60 seconds. Using 60 seconds.")
            seconds = 60
    except ValueError:
        print("⚠️ Invalid input! Using default 20 seconds. ")
        seconds = 20

    # Generate the selected key
    key_generators = {
        1: generate_random_key,
        2: generate_uuid_key,
        3: generate_hex_key,
        4: generate_sha256_key,
        5: generate_base64_key,
        6: generate_numeric_key,
        7: generate_passphrase,
        8: generate_hmac_key,
    }
    key = key_generators[choice]()  # Call the selected function

    # Display the generated key
    print("\n🔑 Generated Key (Copy it now! It will be destroyed soon):\n")
    print(f"📌 {key}\n")
    print(f"⚠️ WARNING: You have {seconds} seconds to copy the key before it is permanently erased.")

    # Start countdown in a separate thread
    timer_thread = threading.Thread(target=countdown_timer, args=(seconds,))
    timer_thread.start()

    # Wait for the countdown to finish
    timer_thread.join()

    # Securely erase key from memory
    wipe_key_from_memory(key)

    # Clear terminal history for security
    if os.name == "posix":  # Linux/Mac
        os.system("history -c && clear")
    elif os.name == "nt":  # Windows
        os.system("cls")

    print("\n✅ Key erased. Gone. Like everyone's hopes at 9AM Monday.\n")
    sys.exit(0)

if __name__ == "__main__":
    main()