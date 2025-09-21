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
    # DRF va chercher automatiquement une méthode qui s’appelle get_author et dont la valeur retournée sera insérée dans la réponse JSON
    author = serializers.SerializerMethodField()
    publication_date_str = serializers.SerializerMethodField()
    
    class Meta:
        """
        Metadata for the ArticleSerializer.

        - model: The model being serialized (Article).
        - fields: All fields on the model are included in the serialized output.
        """
        model = Article
        fields = ["id", "publication_date", "publication_date_str", "title", "content", "author"]
        read_only_fields = ["publication_date_str", "author"]

    def get_author(self, obj):
        if obj.author:
            full_name = f"{obj.author.first_name} {obj.author.last_name}".strip()
            return full_name or obj.author.email
        return None
    
    def get_publication_date_str(self, obj):
        # convertit en fuseau local (TIME_ZONE des settings)
        local_dt = timezone.localtime(obj.publication_date)
        # Ex: "Le 2 septembre 2005 à 15h00"
        # `date_format` respecte la langue active (ex: 'fr') et les formats locaux
        txt = date_format(local_dt, "j F Y \\à H\\hi", use_l10n=True)
        return f"Le {txt}"