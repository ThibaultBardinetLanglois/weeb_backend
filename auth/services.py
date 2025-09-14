from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed, APIException
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AccountInactive(APIException):
    status_code = 403
    default_detail = "Votre compte est en attente de validation par l'administrateur."

def login_and_issue_tokens(request, email, password):
    email = email.lower()

    # 1) Le mail existe t'il en base de données ?
    try:
        user_obj = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        authenticate(request=request, email=email, password=password)  # pour Axes
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # 2) Vérification du mot de passe
    if not user_obj.check_password(password):
        authenticate(request=request, email=email, password=password)  # pour Axes
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # 3) Si le compte existe et est inactif on lève une exception avec le code 403
    if not user_obj.is_active:
        raise AccountInactive()

    # 4) Auth finale + tokens
    user = authenticate(request=request, email=email, password=password)
    if not user:
        raise AuthenticationFailed("Email ou mot de passe incorrect.")

    # Émettre tokens
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    
    # Claims
    access["email"] = user.email
    access["first_name"] = user.first_name
    access["last_name"] = user.last_name

    return {
        "refresh": refresh,
        "response_data": {
            "access": str(access),
            "user": {
                "first_name": user.first_name,
                "last_name":  user.last_name,
                "email":      user.email,
            },
        }
    }
