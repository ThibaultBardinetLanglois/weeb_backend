import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from articles.models import Article

# All tests in this file require access to the test database
pytestmark = pytest.mark.django_db


def test_article_str_representation():
    """The string representation of an article should be its title."""
    article = Article(title="My Article", content="Some content")
    assert str(article) == "My Article"


def test_article_can_be_created_with_author(user):
    """An article can be created with an associated author."""
    article = Article.objects.create(
        title="Article with author",
        content="Content",
        author=user
    )

    assert article.id is not None
    assert article.author == user


def test_article_can_be_created_without_author():
    """An article can be created without an author (anonymous article)."""
    article = Article.objects.create(
        title="Anonymous article",
        content="Content"
    )

    assert article.author is None


def test_article_requires_title():
    """The title field is mandatory."""
    article = Article(content="Content without title")

    with pytest.raises(ValidationError):
        article.full_clean()


def test_article_requires_content():
    """The content field is mandatory."""
    article = Article(title="Title without content")

    with pytest.raises(ValidationError):
        article.full_clean()


def test_article_rejects_empty_title():
    """An empty title should not be accepted."""
    article = Article(title="", content="Content")

    with pytest.raises(ValidationError):
        article.full_clean()


def test_article_rejects_empty_content():
    """An empty content should not be accepted."""
    article = Article(title="Title", content="")

    with pytest.raises(ValidationError):
        article.full_clean()


def test_article_title_max_length():
    """The title must not exceed the maximum allowed length."""
    article = Article(
        title="a" * 256,  # max_length is 255
        content="Content"
    )

    with pytest.raises(ValidationError):
        article.full_clean()


def test_publication_date_is_set_by_default():
    """The publication date should be automatically set on creation."""
    article = Article.objects.create(
        title="Dated article",
        content="Content"
    )

    assert article.publication_date is not None
    assert article.publication_date <= timezone.now()


def test_article_can_have_custom_publication_date():
    """An article can be created with a custom publication date."""
    custom_date = timezone.now() - timezone.timedelta(days=1)

    article = Article.objects.create(
        title="Old article",
        content="Content",
        publication_date=custom_date
    )

    assert article.publication_date == custom_date


def test_article_author_is_set_to_null_when_user_is_deleted(user):
    """If the author is deleted, the article author should be set to NULL."""
    article = Article.objects.create(
        title="Article",
        content="Content",
        author=user
    )

    user.delete()
    article.refresh_from_db()

    assert article.author is None


def test_user_can_access_related_articles(user):
    """The related_name allows accessing articles from the user object."""
    Article.objects.create(
        title="Article 1",
        content="Content",
        author=user
    )
    Article.objects.create(
        title="Article 2",
        content="Content",
        author=user
    )

    assert user.articles.count() == 2


def test_article_accepts_long_content(user):
    """The article content can be very long without raising validation errors."""
    article = Article(
        title="Long content article",
        content="Lorem ipsum " * 1000,
        author=user
    )

    # Should not raise any exception
    article.full_clean()
