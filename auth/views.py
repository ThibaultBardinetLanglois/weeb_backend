import os

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer
from .services import login_and_issue_tokens

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH     = "/api/auth/token/refresh/"

class LoginView(generics.GenericAPIView):
    """
    Authenticate a user with email and password, then issue tokens.

    On success:
      - Returns the access token in the response body.
      - Sets the refresh token in an HttpOnly cookie restricted to the refresh endpoint.
    """
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        
        # Some middleware can wrap the underlying Django request object;
        # make sure we pass the raw request to authentication helpers.
        django_request = getattr(request, "_request", request)
        
        data = login_and_issue_tokens(
            django_request, 
            s.validated_data["email"], 
            s.validated_data["password"]
        )
        
        resp = Response(data["response_data"], status=status.HTTP_200_OK)
        resp.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=data["refresh"],
            max_age=int(os.getenv("COOKIE_REFRESH_MAX_AGE")),
            httponly=True,
            secure=os.getenv("COOKIE_SECURE"),
            samesite=os.getenv("COOKIE_SAMESITE"),
            # Cookie will only be sent when the request path starts with this prefix
            path=REFRESH_COOKIE_PATH  
        )
        return resp
        

class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.

    Returns a message indicating whether the account is pending admin approval.
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(
            {
                "message": "Compte créé. En attente de validation par l’administrateur." if not user.is_active else "Compte créé.",
                "user": {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                },
            },
            
            status=status.HTTP_201_CREATED,
        )
        
        
class CookieTokenRefreshView(APIView):
    """
    Read the 'refresh_token' from an HttpOnly cookie and return a new access token.

    If ROTATE_REFRESH_TOKENS=True, issues a new refresh token and sets it back
    into the cookie (optionally blacklisting the previous one when
    BLACKLIST_AFTER_ROTATION=True).
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_cookie = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if not refresh_cookie:
            return Response(
                {"detail": "Jeton de rafraîchissement manquant."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        try:
            refresh = RefreshToken(refresh_cookie)
            user_id = refresh[api_settings.USER_ID_CLAIM]
            user = User.objects.get(pk=user_id)

            # Build a new access token with custom claims
            access = refresh.access_token
            access["email"] = user.email
            access["first_name"] = user.first_name
            access["last_name"] = user.last_name

            data = {"access": str(access)}
            resp = Response(data, status=status.HTTP_200_OK)

            # If rotation is enabled, blacklist the old refresh (optional)
            # and set a brand new refresh token in the cookie.
            if api_settings.ROTATE_REFRESH_TOKENS:
                refresh.blacklist() if api_settings.BLACKLIST_AFTER_ROTATION else None
                new_refresh = RefreshToken.for_user(user)
                resp.set_cookie(
                    key=REFRESH_COOKIE_NAME,
                    value=str(new_refresh),
                    max_age=int(os.getenv("COOKIE_REFRESH_MAX_AGE", "604800")),
                    httponly=True,
                    # Convert env string to bool: "True"/"true"/"1" => True
                    secure = os.getenv("COOKIE_SECURE", "False").lower() in ("1", "true", "yes"), 
                    samesite=os.getenv("COOKIE_SAMESITE", "Lax"),
                    path=REFRESH_COOKIE_PATH,
                )

            return resp
        except (InvalidToken, TokenError) as e: 
            # Return 401 instead of 500 for expired/invalid refresh tokens,
            # and ensure the client cookie is cleared to avoid retry loops.
            resp = Response(
                {"detail": "Refresh token invalide ou expiré.", "code": "token_not_valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
            # Nettoie le cookie côté client pour éviter des tentatives en boucle
            resp.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        return resp
    
    
class LogoutView(APIView):
    """
    Invalidate the session by removing the refresh cookie and blacklisting the token.

    The endpoint:
      - Blacklists the refresh token if present.
      - Deletes the refresh cookie on the client.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if refresh:
            try:
                # Instantiate a SimpleJWT RefreshToken from the cookie value
                # to access blacklist() and mark it as invalid for future use.
                token = RefreshToken(refresh)
                token.blacklist()  # adds an entry in BlacklistedToken
            except TokenError:
                # Token already invalid/expired—no need to blacklist further.
                pass

        resp = Response({"detail": "Déconnecté."}, status=status.HTTP_200_OK)
        resp.delete_cookie(key=REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        
        return resp
        