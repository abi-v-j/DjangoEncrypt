from django.shortcuts import render
from django.core.files.storage import default_storage
from .crypto_utils import (
    generate_key,
    encrypt_text,
    decrypt_text,
    encrypt_file,
    decrypt_file,
    encrypt_folder,
    decrypt_folder,
)
import os
import shutil
from django.conf import settings


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
            return render(
                request, "encryption_app/index.html", {"error": "Text and Key are required!"}
            )
        try:
            encrypted_text = encrypt_text(text, key)
            return render(
                request,
                "encryption_app/index.html",
                {"encrypted_text": encrypted_text, "key": key},
            )
        except ValueError as e:
            return render(request, "encryption_app/index.html", {"error": str(e)})
    return render(request, "encryption_app/index.html")


def decrypt_view(request):
    """Decrypt the encrypted text."""
    if request.method == "POST":
        encrypted_text = request.POST.get("encrypted_text")
        key = request.POST.get("key")
        if not encrypted_text or not key:
            return render(
                request, "encryption_app/index.html", {"error": "Encrypted Text and Key are required!"}
            )
        try:
            decrypted_text = decrypt_text(encrypted_text, key)
            return render(
                request,
                "encryption_app/index.html",
                {"decrypted_text": decrypted_text, "key": key},
            )
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
        return render(
            request,
            "encryption_app/index.html",
            {"encrypted_file": os.path.basename(encrypted_file_path), "key": key},
        )
    return render(
        request, "encryption_app/index.html", {"error": "File and key are required for encryption."}
    )


def decrypt_file_view(request):
    """Decrypt an uploaded encrypted file."""
    if request.method == "POST" and request.FILES.get("file") and request.POST.get("key"):
        file = request.FILES["file"]
        key = request.POST["key"]
        file_path = default_storage.save(file.name, file)
        decrypted_file_path = decrypt_file(file_path, key)
        return render(
            request,
            "encryption_app/index.html",
            {"decrypted_file": os.path.basename(decrypted_file_path), "key": key},
        )
    return render(
        request, "encryption_app/index.html", {"error": "File and key are required for decryption."}
    )

def encrypt_folder_view(request):
    """Encrypt an uploaded folder."""
    if request.method == "POST" and request.FILES.getlist("files") and request.POST.get("key"):
        files = request.FILES.getlist("files")
        key = request.POST["key"]

        # Create a temporary folder to store uploaded files
        temp_folder = os.path.join(settings.MEDIA_ROOT, "temp_folder")
        os.makedirs(temp_folder, exist_ok=True)

        try:
            # Save uploaded files to the temporary folder while preserving directory structure
            for file in files:
                # Extract the relative path from the file name
                relative_path = file.name
                file_path = os.path.join(temp_folder, relative_path)

                # Ensure the directory structure exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Save the file
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

            # Encrypt the folder
            encrypted_folder_path = encrypt_folder(temp_folder, key)

            # Provide a download link for the encrypted folder
            encrypted_folder_name = os.path.basename(encrypted_folder_path)
            download_url = default_storage.url(encrypted_folder_name)

            return render(
                request,
                "encryption_app/index.html",
                {
                    "encrypted_folder": encrypted_folder_name,
                    "download_url": download_url,
                    "key": key,
                },
            )
        finally:
            # Clean up the temporary folder
            shutil.rmtree(temp_folder, ignore_errors=True)

    return render(
        request, "encryption_app/index.html", {"error": "Files and key are required for folder encryption."}
    )


def decrypt_folder_view(request):
    """Decrypt an uploaded encrypted folder."""
    if request.method == "POST" and request.FILES.getlist("files") and request.POST.get("key"):
        files = request.FILES.getlist("files")
        key = request.POST["key"]

        # Create a temporary folder to store uploaded files
        temp_folder = os.path.join(settings.MEDIA_ROOT, "temp_folder_encrypted")
        os.makedirs(temp_folder, exist_ok=True)

        try:
            # Save uploaded files to the temporary folder while preserving directory structure
            for file in files:
                # Extract the relative path from the file name
                relative_path = file.name
                file_path = os.path.join(temp_folder, relative_path)

                # Ensure the directory structure exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Save the file
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

            # Decrypt the folder
            decrypted_folder_path = decrypt_folder(temp_folder, key)

            # Provide a download link for the decrypted folder
            decrypted_folder_name = os.path.basename(decrypted_folder_path)
            download_url = default_storage.url(decrypted_folder_name)

            return render(
                request,
                "encryption_app/index.html",
                {
                    "decrypted_folder": decrypted_folder_name,
                    "download_url": download_url,
                    "key": key,
                },
            )
        finally:
            # Clean up the temporary folder
            shutil.rmtree(temp_folder, ignore_errors=True)

    return render(
        request, "encryption_app/index.html", {"error": "Files and key are required for folder decryption."}
    )