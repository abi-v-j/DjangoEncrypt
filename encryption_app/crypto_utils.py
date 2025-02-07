import base64
import os
from cryptography.fernet import Fernet
from pathlib import Path

def generate_key():
    """Generate a valid 32-byte Base64-encoded key for encryption."""
    return Fernet.generate_key().decode()

def validate_and_encode_key(key):
    """Ensure the key is 32 bytes and Base64-encoded."""
    try:
        decoded_key = base64.urlsafe_b64decode(key)
        if len(decoded_key) == 32:
            return key  # Key is already valid
        else:
            raise ValueError("Invalid key: The key must be exactly 32 bytes after decoding.")
    except Exception as e:
        raise ValueError(f"Invalid key: {str(e)}")

def encrypt_text(text, key):
    """Encrypt a given text using a valid key."""
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    """Decrypt a given text using a valid key."""
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    return cipher.decrypt(encrypted_text.encode()).decode()

def encrypt_file(file_path, key):
    """Encrypt a file and save it with '.enc' extension."""
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    with open(file_path, 'rb') as f:
        encrypted_data = cipher.encrypt(f.read())
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    return encrypted_file_path

def decrypt_file(encrypted_file_path, key):
    """Decrypt a file and restore the original filename."""
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    with open(encrypted_file_path, 'rb') as f:
        decrypted_data = cipher.decrypt(f.read())
    if encrypted_file_path.endswith(".enc"):
        original_file_path = encrypted_file_path[:-4]
    else:
        original_file_path = encrypted_file_path.replace("_decrypted", "")
    with open(original_file_path, 'wb') as f:
        f.write(decrypted_data)
    return original_file_path

def encrypt_folder(folder_path, key):
    """
    Encrypt all files in a folder and save them in a new folder with '.enc' suffix.
    """
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    
    # Create a new folder for encrypted files
    encrypted_folder_path = folder_path + ".enc"
    os.makedirs(encrypted_folder_path, exist_ok=True)
    
    # Walk through the folder and encrypt each file
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)
            encrypted_file_path = os.path.join(encrypted_folder_path, relative_path)
            
            # Ensure the directory structure exists
            os.makedirs(os.path.dirname(encrypted_file_path), exist_ok=True)
            
            # Encrypt the file
            with open(file_path, 'rb') as f:
                encrypted_data = cipher.encrypt(f.read())
            with open(encrypted_file_path, 'wb') as f:
                f.write(encrypted_data)
    
    return encrypted_folder_path

def decrypt_folder(encrypted_folder_path, key):
    """
    Decrypt all files in an encrypted folder and save them in a new folder without '.enc' suffix.
    """
    key = validate_and_encode_key(key)
    cipher = Fernet(key.encode())
    
    # Create a new folder for decrypted files
    if encrypted_folder_path.endswith(".enc"):
        decrypted_folder_path = encrypted_folder_path[:-4]
    else:
        decrypted_folder_path = encrypted_folder_path + "_decrypted"
    os.makedirs(decrypted_folder_path, exist_ok=True)
    
    # Walk through the encrypted folder and decrypt each file
    for root, _, files in os.walk(encrypted_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, encrypted_folder_path)
            decrypted_file_path = os.path.join(decrypted_folder_path, relative_path)
            
            # Ensure the directory structure exists
            os.makedirs(os.path.dirname(decrypted_file_path), exist_ok=True)
            
            # Decrypt the file
            with open(file_path, 'rb') as f:
                decrypted_data = cipher.decrypt(f.read())
            with open(decrypted_file_path, 'wb') as f:
                f.write(decrypted_data)
    
    return decrypted_folder_path