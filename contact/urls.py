from django.urls import path
from .views import contact_message_create


# URL patterns for the contact app
urlpatterns = [
    # Endpoint to handle contact form submissions (POST only)
    path('', contact_message_create, name='contact_message_create'),
]
