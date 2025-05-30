"""
Views for the articles app.

This module defines viewsets that expose CRUD operations for the Article model
using Django REST Framework.
"""

from rest_framework import viewsets, filters
from .models import Article
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on Article instances.

    This class automatically provides 'list', 'create', 'retrieve',
    'update', and 'destroy' actions via DRF's ModelViewSet.
    It also supports search and ordering via query parameters.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    # Enable search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author']           # e.g., ?search=python
    ordering_fields = ['publication_date', 'title']          # e.g., ?ordering=-title
