import os

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import EmailTokenObtainPairSerializer, RegisterSerializer
from .services import login_and_issue_tokens

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH     = "/api/token/refresh/"

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
            path=REFRESH_COOKIE_PATH  # accessible uniquement sur ce endpoint,
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

        ser = TokenRefreshSerializer(data={"refresh": refresh_cookie})
        ser.is_valid(raise_exception=True)

        data = {"access": ser.validated_data["access"]}

        # Rotation active => SimpleJWT renvoie un nouveau refresh
        new_refresh = ser.validated_data.get("refresh")
        resp = Response(data, status=status.HTTP_200_OK)

        if new_refresh:
            resp.set_cookie(
                key=REFRESH_COOKIE_NAME,
                value=new_refresh,
                max_age=int(os.getenv("COOKIE_REFRESH_MAX_AGE")),
                httponly=True,
                secure=os.getenv("COOKIE_SECURE"),
                samesite=os.getenv("COOKIE_SAMESITE"),
                path=REFRESH_COOKIE_PATH,
            )
        return resp
    
    
class LogoutView(APIView):
    """
    Supprime le cookie de refresh côté client.
    Il faut Penser à blacklister le refresh token du cookie.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(REFRESH_COOKIE_NAME)

        if refresh:
            try:
                token = RefreshToken(refresh)
                token.blacklist()  # ajoute dans BlacklistedToken
            except TokenError:
                # Jeton déjà expiré/invalidé, on passe à l'étape suivante
                pass

        resp = Response({"detail": "Déconnecté."}, status=status.HTTP_200_OK)
        resp.delete_cookie(key=REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)
        return resp
        