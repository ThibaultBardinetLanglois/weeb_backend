"""
Serializers for the Article model.

Defines how Article instances are converted to and from JSON representations
for use in the Django REST Framework API.
"""

from rest_framework import serializers
from .models import Article
from django.utils import timezone
from django.utils.formats import date_format


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Adds custom fields:
        - author: Human-readable name or email of the author.
        - publication_date_str: Localized, human-friendly string for the publication date.
    """
    # DRF will automatically call the method `get_author` and inject its
    # return value into the serialized output.
    author = serializers.SerializerMethodField()
    publication_date_str = serializers.SerializerMethodField()
    
    class Meta:
        """
        Metadata for the ArticleSerializer.

        - model: The model being serialized (Article).
        - fields: All fields on the model are included in the serialized output.
        - read_only_fields (list): Fields that cannot be updated via the API.
        """
        model = Article
        fields = ["id", "publication_date", "publication_date_str", "title", "content", "author"]
        read_only_fields = ["publication_date_str", "author"]

    def get_author(self, obj):
        """
        Return the author's full name if available,
        otherwise fall back to their email address.
        """
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name or obj.author.email
        return None
    
    def get_publication_date_str(self, obj):
        """
        Return a localized, human-friendly string for the publication date.

        Example (French locale): "Le 2 septembre 2005 à 15h00"
        """
        local_dt = timezone.localtime(obj.publication_date)
        txt = date_format(local_dt, "j F Y \\à H\\hi", use_l10n=True)
        return f"Le {txt}"