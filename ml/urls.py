from django.urls import path
from .views import sentiment_analysis

urlpatterns = [
    path('sentiment-analysis', sentiment_analysis, name='sentiment-analysis'),
]
