from rest_framework import serializers
from .models import Contact
import re

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    This handles validation and serialization/deserialization of contact form data.
    Includes custom error messages and format checks for phone and email fields.
    """
    
    # Field-level validations with custom French error messages
    first_name = serializers.CharField(
        max_length=99,
        error_messages={
            "required": "Le prénom est obligatoire.",
            "blank": "Le prénom ne peut pas être vide.",
            "max_length": "Le prénom ne peut pas dépasser 99 caractères.",
        }
    )
    last_name = serializers.CharField(
        max_length=99,
        error_messages={
            "required": "Le nom est obligatoire.",
            "blank": "Le nom ne peut pas être vide.",
            "max_length": "Le nom ne peut pas dépasser 99 caractères.",
        }
    )
    phone = serializers.CharField(
        error_messages={
            "required": "Le téléphone est obligatoire.",
            "blank": "Le téléphone ne peut pas être vide.",
        }
    )
    email = serializers.EmailField(
        error_messages={
            "required": "L'adresse email est obligatoire.",
            "blank": "L'adresse email ne peut pas être vide.",
            "invalid": "L'adresse email est invalide.",
        }
    )
    message = serializers.CharField(
        max_length=999,
        error_messages={
            "required": "Le message est obligatoire.",
            "blank": "Le message ne peut pas être vide.",
            "max_length": "Le message ne peut pas dépasser 999 caractères.",
        }
    )

    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at'] # created_at is auto-set, not user-editable

    def validate_phone(self, value):
        """
        Validates the phone number format using a regex pattern.
        Expects an international format (e.g., +33123456789).
        """
        pattern = r'^\+?\d{9,15}$'  
        if not re.match(pattern, value):
            raise serializers.ValidationError("Le numéro de téléphone est invalide. Utilisez le format international.")
        return value

    def validate_email(self, value):
        """
        Adds a custom error message for invalid email formats.
        While EmailField already validates the format, this ensures French feedback.
        """
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("L'adresse email est invalide.")
        return value
