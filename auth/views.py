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
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        django_request = getattr(request, "_request", request)
        data = login_and_issue_tokens(django_request, s.validated_data["email"], s.validated_data["password"])
        
        resp = Response(data["response_data"], status=status.HTTP_200_OK)
        resp.set_cookie(
            key=REFRESH_COOKIE_NAME,
            value=data["refresh"],
            max_age=int(os.getenv("COOKIE_REFRESH_MAX_AGE")),
            httponly=True,
            secure=os.getenv("COOKIE_SECURE"),
            samesite=os.getenv("COOKIE_SAMESITE"),
            path=REFRESH_COOKIE_PATH  # accessible uniquement sur ce endpoint, le cookie ne sera envoyé que si l’URL de la requête commence par ce chemin
        )
        return resp
        

class RegisterView(generics.CreateAPIView):
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
    Lit le cookie 'refresh_token' et renvoie un nouvel access.
    Si la rotation est activée (ROTATE_REFRESH_TOKENS=True),
    repose un nouveau refresh dans le cookie.
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

            # créer un nouvel access avec claims personnalisés
            access = refresh.access_token
            access["email"] = user.email
            access["first_name"] = user.first_name
            access["last_name"] = user.last_name

            data = {"access": str(access)}
            resp = Response(data, status=status.HTTP_200_OK)

            # rotation activée => nouveau refresh + blacklist de l’ancien
            if api_settings.ROTATE_REFRESH_TOKENS:
                refresh.blacklist() if api_settings.BLACKLIST_AFTER_ROTATION else None
                new_refresh = RefreshToken.for_user(user)
                resp.set_cookie(
                    key=REFRESH_COOKIE_NAME,
                    value=str(new_refresh),
                    max_age=int(os.getenv("COOKIE_REFRESH_MAX_AGE", "604800")),
                    httponly=True,
                    secure = os.getenv("COOKIE_SECURE", "False").lower() in ("1", "true", "yes"), # Si COOKIE_SECURE vaut "True", "true", ou "1" => secure=True
                    samesite=os.getenv("COOKIE_SAMESITE", "Lax"),
                    path=REFRESH_COOKIE_PATH,
                )

            return resp
        except (InvalidToken, TokenError) as e: 
            # On renvoi un code 401 au lieu de 500, et on supprime le cookie expiré
            resp = Response(
                {"detail": "Refresh token invalide ou expiré.", "code": "token_not_valid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
            # Nettoie le cookie côté client pour éviter des tentatives en boucle
            resp.delete_cookie(REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        return resp
    
    
class LogoutView(APIView):
    """
    Supprime le cookie de refresh côté client.
    Il faut Penser à blacklister le refresh token du cookie.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if refresh:
            try:
                # Instancier un objet RefreshToken (de la lib rest_framework_simplejwt) à partir de la chaîne du jeton refresh récupérée dans le cookie
                # Cette instanciation permet d’accéder à ses méthodes, dont blacklist()
                token = RefreshToken(refresh)
                token.blacklist()  # ajoute dans BlacklistedToken
            except TokenError:
                # Jeton déjà expiré/invalidé, on passe à l'étape suivante car on n’as plus besoin de le blacklister
                pass

        resp = Response({"detail": "Déconnecté."}, status=status.HTTP_200_OK)
        resp.delete_cookie(key=REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        
        return resp
        