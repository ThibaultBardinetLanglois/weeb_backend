from django.urls import path
from .views import hello_contact

urlpatterns = [
    path('', hello_contact, name='hello_contact'),
]
