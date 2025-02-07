from django.urls import path
from .views import (
    home,
    generate_key_view,
    encrypt_view,
    decrypt_view,
    encrypt_file_view,
    decrypt_file_view,
    encrypt_folder_view,
    decrypt_folder_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("generate-key/", generate_key_view, name="generate_key"),
    path("encrypt/", encrypt_view, name="encrypt"),
    path("decrypt/", decrypt_view, name="decrypt"),
    path("encrypt-file/", encrypt_file_view, name="encrypt_file"),
    path("decrypt-file/", decrypt_file_view, name="decrypt_file"),
    path("encrypt-folder/", encrypt_folder_view, name="encrypt_folder"),
    path("decrypt-folder/", decrypt_folder_view, name="decrypt_folder"),
]