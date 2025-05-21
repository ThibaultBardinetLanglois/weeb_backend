from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
#using viewsets to make crud operation routes simpler
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
