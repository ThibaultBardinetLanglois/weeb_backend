import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        email="testuser@example.com",
        password="strong-password",
        first_name="Test",
        last_name="User",
        is_active=True
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """
    Return an authenticated API client.
    The client is logged in as the test user.
    """
    api_client.force_authenticate(user=user)
    return api_client
