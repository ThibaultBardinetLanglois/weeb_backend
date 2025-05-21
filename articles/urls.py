from django.urls import path
from .views import hello_articles

urlpatterns = [
    path('', hello_articles, name='hello_articles'),
]
