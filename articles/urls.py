"""
URL routing for the articles app.

This module defines API endpoints for managing articles using a DRF router.
The base path /api/articles/ is mapped to the ArticleViewSet.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet

# Initialize a default router and register the ArticleViewSet
# The empty string ('') makes the final path /api/articles/
router = DefaultRouter()
router.register(r'', ArticleViewSet)

# Include the router-generated URLs
urlpatterns = [
    path('', include(router.urls)),
]
