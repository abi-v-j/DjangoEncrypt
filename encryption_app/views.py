from django.shortcuts import render
from django.core.files.storage import default_storage
from .crypto_utils import generate_key, encrypt_text, decrypt_text, encrypt_file, decrypt_file
import os

def home(request):
    """Render the encryption & decryption page."""
    return render(request, "encryption_app/index.html")

def generate_key_view(request):
    """Generate a secure encryption key and display it on the page."""
    key = generate_key()
    return render(request, "encryption_app/index.html", {"generated_key": key})

def encrypt_view(request):
    """Encrypt the input text."""
    if request.method == "POST":
        text = request.POST.get("text")
        key = request.POST.get("key")

        if not text or not key:
            return render(request, "encryption_app/index.html", {"error": "Text and Key are required!"})

        try:
            encrypted_text = encrypt_text(text, key)
            return render(request, "encryption_app/index.html", {"encrypted_text": encrypted_text, "key": key})
        except ValueError as e:
            return render(request, "encryption_app/index.html", {"error": str(e)})

    return render(request, "encryption_app/index.html")

def decrypt_view(request):
    """Decrypt the encrypted text."""
    if request.method == "POST":
        encrypted_text = request.POST.get("encrypted_text")
        key = request.POST.get("key")

        if not encrypted_text or not key:
            return render(request, "encryption_app/index.html", {"error": "Encrypted Text and Key are required!"})

        try:
            decrypted_text = decrypt_text(encrypted_text, key)
            return render(request, "encryption_app/index.html", {"decrypted_text": decrypted_text, "key": key})
        except ValueError as e:
            return render(request, "encryption_app/index.html", {"error": str(e)})

    return render(request, "encryption_app/index.html")

def encrypt_file_view(request):
    """Encrypt an uploaded file."""
    if request.method == "POST" and request.FILES.get("file") and request.POST.get("key"):
        file = request.FILES["file"]
        key = request.POST["key"]

        file_path = default_storage.save(file.name, file)
        encrypted_file_path = encrypt_file(file_path, key)

        return render(request, "encryption_app/index.html", {
            "encrypted_file": os.path.basename(encrypted_file_path),
            "key": key
        })

    return render(request, "encryption_app/index.html", {"error": "File and key are required for encryption."})

def decrypt_file_view(request):
    """Decrypt an uploaded encrypted file."""
    if request.method == "POST" and request.FILES.get("file") and request.POST.get("key"):
        file = request.FILES["file"]
        key = request.POST["key"]

        file_path = default_storage.save(file.name, file)
        decrypted_file_path = decrypt_file(file_path, key)

        return render(request, "encryption_app/index.html", {
            "decrypted_file": os.path.basename(decrypted_file_path),
            "key": key
        })

    return render(request, "encryption_app/index.html", {"error": "File and key are required for decryption."})


