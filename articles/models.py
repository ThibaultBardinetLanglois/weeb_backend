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
    Model representing an article entry.

    Fields:
        title (CharField): The article's title.
        content (TextField): The body text of the article.
        author (ForeignKey): Optional reference to the user who wrote the article.
        publication_date (DateTimeField): Date and time of publication,
            defaults to the current time.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="articles"
    )
    publication_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return the string representation of the article (its title)."""
        return self.title
