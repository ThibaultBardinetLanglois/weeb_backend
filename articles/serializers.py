"""
Serializers for the Article model.

Defines how Article instances are converted to and from JSON representations
for use in the Django REST Framework API.
"""

from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Handles validation and transformation of Article objects for API usage.
    The 'publication_date' field is optional on input; if omitted,
    the model default will apply (current date).
    """
    publication_date = serializers.DateField(required=False)

    class Meta:
        """
        Metadata for the ArticleSerializer.

        - model: The model being serialized (Article).
        - fields: All fields on the model are included in the serialized output.
        """
        model = Article
        fields = '__all__'
