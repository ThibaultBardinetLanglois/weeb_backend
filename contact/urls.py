"""
URL configuration for the contact app.

Defines the endpoint for handling contact form submissions.
"""

from django.urls import path
from .views import contact_message_create

urlpatterns = [
    # Endpoint to handle contact form submissions (POST only)
    path('', contact_message_create, name='contact_message_create'),
]
