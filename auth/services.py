from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountInactive(APIException):
    """
    Custom exception raised when a user account exists
    but has not yet been activated by an administrator.
    """
    status_code = 403
    default_detail = "Votre compte est en attente de validation par l'administrateur."
    

def login_and_issue_tokens(request, email, password):
    """
    Authenticate a user by email and password, and issue JWT tokens.

    Steps:
        1. Ensure the email exists in the database.
        2. Verify the provided password.
        3. Check if the account is active, otherwise raise AccountInactive.
        4. Perform final authentication and generate access/refresh tokens.

    The access token includes custom claims (email, first_name, last_name).
    The refresh token is returned separately.
    """
    email = email.lower()

    # 1.
    try:
        user_obj = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        authenticate(request=request, email=email, password=password)  # pour Axes
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # 2.
    if not user_obj.check_password(password):
        authenticate(request=request, email=email, password=password)  # pour Axes
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # 3.
    if not user_obj.is_active:
        raise AccountInactive()

    # 4.
    user = authenticate(request=request, email=email, password=password)
    if not user:
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    # Add custom claims to the access token
    access["email"] = user.email
    access["first_name"] = user.first_name
    access["last_name"] = user.last_name

    return {
        "refresh": refresh,
        "response_data": { "access": str(access) }
    }
