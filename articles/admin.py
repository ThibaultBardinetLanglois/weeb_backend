"""
Admin configuration for the Article model.

This module registers the Article model with the Django admin interface
and customizes how it is displayed and searched in the admin panel.
"""

from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin view configuration for the Article model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields that can be searched via the admin interface.
    """
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author', 'content')
