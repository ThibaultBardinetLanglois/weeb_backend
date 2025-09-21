"""
URL configuration for the auth app.

Defines authentication-related API endpoints:
- register: Create a new user account
- login: Authenticate and issue tokens
- token/refresh: Refresh the access token using a cookie-based refresh token
- logout: Invalidate the session and remove the refresh token
"""

from django.urls import path
from .views import LoginView, RegisterView, LogoutView, CookieTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogoutView.as_view(), name="logout"),
]
