from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountInactive(APIException):
    status_code = 403
    default_detail = "Votre compte est en attente de validation par l'administrateur."
    default_code = "account_inactive"

# Connexion
class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={"required": "L'email est obligatoire."})
    password = serializers.CharField(required=True, write_only=True, error_messages={"required": "Le mot de passe est obligatoire."})


# Enregistrement
class RegisterSerializer(serializers.Serializer):
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
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return email

    def validate(self, attrs):
        fn = (attrs.get("firstname") or "").strip()
        ln = (attrs.get("lastname") or "").strip()
        if not fn:
            raise serializers.ValidationError({"firstname": "Le prénom ne peut pas être vide."})
        if not ln:
            raise serializers.ValidationError({"lastname": "Le nom ne peut pas être vide."})

        # Valider le mot de passe via les validators Django configurés (base.py)
        temp_user = User(email=attrs["email"].lower(), first_name=fn, last_name=ln)
        validate_password(attrs["password"], user=temp_user)
        return attrs
    
    def create(self, validated_data):
        email = validated_data["email"].lower()
        user = User.objects.create_user(
            email=email,
            password=validated_data["password"],
            first_name=validated_data["firstname"].strip(),
            last_name=validated_data["lastname"].strip(),
            is_active=False,
        )
        
        return user