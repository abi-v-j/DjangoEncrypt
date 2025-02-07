import base64
import os
from cryptography.fernet import Fernet

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
    except Exception:
        raise ValueError("Invalid key: Must be a 32-byte Base64-encoded key.")

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

    # Remove ".enc" to get original filename
    if encrypted_file_path.endswith(".enc"):
        original_file_path = encrypted_file_path[:-4]  # Remove ".enc"
    else:
        original_file_path = encrypted_file_path.replace("_decrypted", "")  # Fallback case

    with open(original_file_path, 'wb') as f:
        f.write(decrypted_data)

    return original_file_path
