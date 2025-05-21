from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    publication_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
