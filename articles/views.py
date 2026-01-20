"""
Views for the articles app.

This module defines viewsets that expose CRUD operations for the Article model
using Django REST Framework.
"""

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    
    # Default ordering: most recent first
    ordering = ['-publication_date']  

    # Enable search and ordering filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']                    # e.g., ?search=python
    ordering_fields = ['publication_date', 'title']         # e.g., ?ordering=-title
    
    def get_permissions(self):
        """
        Define access rules:
        - Read operations (list/retrieve): open to all users.
        - Write operations (create/update/destroy): require authentication.
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """
        Automatically associate the logged-in user as the author
        when creating a new article.
        """
        serializer.save(author=self.request.user)
