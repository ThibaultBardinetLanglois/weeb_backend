import pytest
from django.urls import reverse
from rest_framework import status
from contact.models import Contact

# All tests in this file require database access
pytestmark = pytest.mark.django_db


def test_contact_message_can_be_created(api_client):
    """A valid contact message can be created via the API."""
    url = reverse("contact_message_create")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "0123456789",
        "email": "john.doe@example.com",
        "message": "Hello, this is a test message."
    }

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "Message reçu avec succès."
    assert Contact.objects.count() == 1


def test_contact_message_creation_fails_with_missing_fields(api_client):
    """Missing required fields should return validation errors."""
    url = reverse("contact_message_create")
    data = {
        "first_name": "John",
        "email": "john@example.com"
    }

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "last_name" in response.data
    assert "message" in response.data


def test_contact_message_creation_fails_with_invalid_email(api_client):
    """Invalid email format should be rejected."""
    url = reverse("contact_message_create")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "0123456789",
        "email": "invalid-email",
        "message": "Message"
    }

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


def test_contact_message_rejects_too_long_message(api_client):
    """Serializer enforces max_length validation on the message field."""
    url = reverse("contact_message_create")
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "0123456789",
        "email": "john@example.com",
        "message": "A" * 1500
    }

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "message" in response.data 


def test_contact_endpoint_only_accepts_post(api_client):
    """GET requests are not allowed on the contact endpoint."""
    url = reverse("contact_message_create")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
