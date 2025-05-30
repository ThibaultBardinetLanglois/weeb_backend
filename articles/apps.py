"""
App configuration for the articles app.

This module defines the configuration for the Django 'articles' app,
used to manage article-related models, views, and other resources.
"""

from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """
    Configuration class for the articles app.

    Attributes:
        default_auto_field (str): The default type of primary key field to use for models.
        name (str): The full Python path to the app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"
