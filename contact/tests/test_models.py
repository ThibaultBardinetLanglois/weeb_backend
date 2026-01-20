import pytest
from django.core.exceptions import ValidationError
from contact.models import Contact

# All tests in this file require database access
pytestmark = pytest.mark.django_db


def test_contact_str_representation():
    """The string representation of a contact should be 'first_name last_name'."""
    contact = Contact.objects.create(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        email="john.doe@example.com",
        message="Hello"
    )

    assert str(contact) == "John Doe"


def test_contact_can_be_created():
    """A contact instance can be created with valid data."""
    contact = Contact.objects.create(
        first_name="Jane",
        last_name="Smith",
        phone="0612345678",
        email="jane.smith@example.com",
        message="This is a test message"
    )

    assert contact.id is not None
    assert contact.email == "jane.smith@example.com"


def test_contact_requires_first_name():
    """First name is mandatory."""
    contact = Contact(
        last_name="Doe",
        phone="0123456789",
        email="test@example.com",
        message="Message"
    )

    with pytest.raises(ValidationError):
        contact.full_clean()


def test_contact_requires_last_name():
    """Last name is mandatory."""
    contact = Contact(
        first_name="John",
        phone="0123456789",
        email="test@example.com",
        message="Message"
    )

    with pytest.raises(ValidationError):
        contact.full_clean()


def test_contact_requires_email():
    """Email is mandatory."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        message="Message"
    )

    with pytest.raises(ValidationError):
        contact.full_clean()


def test_contact_email_must_be_valid():
    """Email must respect a valid email format."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        email="invalid-email",
        message="Message"
    )

    with pytest.raises(ValidationError):
        contact.full_clean()


def test_contact_requires_message():
    """Message field is mandatory."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        email="john@example.com"
    )

    with pytest.raises(ValidationError):
        contact.full_clean()


def test_contact_accepts_long_message():
    """TextField does not enforce max_length at model validation level."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        email="john@example.com",
        message="A" * 1000
    )

    # Should not raise any validation error
    contact.full_clean()


def test_contact_accepts_valid_phone_number():
    """Phone number is stored as-is (no validation at model level)."""
    contact = Contact.objects.create(
        first_name="John",
        last_name="Doe",
        phone="+33 6 12 34 56 78",
        email="john@example.com",
        message="Message"
    )

    assert contact.phone == "+33 6 12 34 56 78"


def test_contact_created_at_is_set_automatically():
    """created_at should be automatically set when the object is created."""
    contact = Contact.objects.create(
        first_name="John",
        last_name="Doe",
        phone="0123456789",
        email="john@example.com",
        message="Message"
    )

    assert contact.created_at is not None
