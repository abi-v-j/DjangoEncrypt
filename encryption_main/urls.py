
from django.urls import path,include

urlpatterns = [
    path('', include("encryption_app.urls")),
]
