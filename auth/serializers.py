from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountInactive(APIException):
    """
    Custom exception raised when a user account exists but has not yet
    been activated by an administrator.
    """
    status_code = 403
    default_detail = "Votre compte est en attente de validation par l'administrateur."
    default_code = "account_inactive"

# ------------------------------
# Login
# ------------------------------
class EmailTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializer for authenticating a user with email and password.

    Returns a token pair (access/refresh) if authentication is successful.
    """
    email = serializers.EmailField(required=True, error_messages={"required": "L'email est obligatoire."})
    
    # `write_only=True` → field must be provided on input but is never returned
    password = serializers.CharField(required=True, write_only=True, error_messages={"required": "Le mot de passe est obligatoire."})


# ------------------------------
# Registration
# ------------------------------
class RegisterSerializer(serializers.Serializer):
    """
    Serializer for registering a new user account.
    Validates email uniqueness, non-empty names, and password strength.
    """
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "L'email est obligatoire.",
            "invalid": "Format d'email invalide.",
        },
    )
    
    firstname = serializers.CharField(
        required=True,
        error_messages={"required": "Le prénom est obligatoire."},
    )
    
    lastname = serializers.CharField(
        required=True,
        error_messages={"required": "Le nom est obligatoire."},
    )
    
    password = serializers.CharField(
        required=True, write_only=True,
        error_messages={"required": "Le mot de passe est obligatoire."},
    )

    def validate_email(self, value):
        """
        Ensure the email is unique (case-insensitive).
        """
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return email

    def validate(self, attrs):
        """
        Perform global validation:
        - Ensure first/last names are not empty after trimming.
        - Validate password strength against Django's configured validators.
        """
        fn = (attrs.get("firstname") or "").strip()
        ln = (attrs.get("lastname") or "").strip()
        if not fn:
            raise serializers.ValidationError({"firstname": "Le prénom ne peut pas être vide."})
        if not ln:
            raise serializers.ValidationError({"lastname": "Le nom ne peut pas être vide."})

        # Validate password strength using Django's password validators
        temp_user = User(email=attrs["email"].lower(), first_name=fn, last_name=ln)
        validate_password(attrs["password"], user=temp_user)
        return attrs
    
    def create(self, validated_data):
        """
        Create a new inactive user account (awaiting admin approval).
        """
        email = validated_data["email"].lower()
        user = User.objects.create_user(
            email=email,
            password=validated_data["password"],
            first_name=validated_data["firstname"].strip(),
            last_name=validated_data["lastname"].strip(),
            is_active=False,
        )
        
        return user