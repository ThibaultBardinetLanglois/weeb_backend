"""
Serializers for the Article model.

Defines how Article instances are converted to and from JSON representations
for use in the Django REST Framework API.
"""

from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    # DRF va chercher automatiquement une méthode qui s’appelle get_author et dont la valeur retournée sera insérée dans la réponse JSON
    author = serializers.SerializerMethodField()
    
    class Meta:
        """
        Metadata for the ArticleSerializer.

        - model: The model being serialized (Article).
        - fields: All fields on the model are included in the serialized output.
        """
        model = Article
        fields = ["id", "publication_date", "title", "content", "author"]

    def get_author(self, obj):
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name or obj.author.email
        return None