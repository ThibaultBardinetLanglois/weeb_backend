# auth/urls.py
from django.urls import path
from .views import LoginView, RegisterView, LogoutView, CookieTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
]
