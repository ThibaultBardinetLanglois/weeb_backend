from django.db import models
from django.conf import settings
from django.utils import timezone


def get_today_date():
    """
    Returns the current date without time component.
    Used as the default value for publication_date.
    """
    return timezone.now().date()


class Article(models.Model):
    """
    Represents an article with a title, content, optional author,
    and an optional publication date that defaults to today.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="articles"
    )
    publication_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
