import pytest
from django.urls import reverse
from rest_framework import status
from articles.models import Article

# All tests in this file require access to the test database
pytestmark = pytest.mark.django_db


# ============================
# READ OPERATIONS (PUBLIC)
# ============================

def test_article_list_is_public(api_client):
    """Unauthenticated users can list articles.
    reverse function generate the API endpoint URL from its name, instead of hardcoding the URL.
    """
    
    url = reverse("article-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


def test_article_detail_is_public(api_client, user):
    """Unauthenticated users can retrieve a single article."""
    article = Article.objects.create(
        title="Public article",
        content="Content",
        author=user
    )

    url = reverse("article-detail", args=[article.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == article.title


# ============================
# CREATE (AUTH REQUIRED)
# ============================

def test_article_creation_requires_authentication(api_client):
    """Unauthenticated users cannot create articles."""
    url = reverse("article-list")
    data = {
        "title": "New article",
        "content": "Content"
    }

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_create_article(authenticated_client, user):
    """Authenticated users can create articles."""
    url = reverse("article-list")
    data = {
        "title": "Created article",
        "content": "Content"
    }

    response = authenticated_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Article.objects.count() == 1

    article = Article.objects.first()
    assert article.title == data["title"]
    assert article.author == user


def test_article_author_is_set_automatically(authenticated_client, user):
    """The author field is automatically set to the logged-in user."""
    url = reverse("article-list")
    data = {
        "title": "Article",
        "content": "Content"
    }

    response = authenticated_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    article = Article.objects.first()
    assert article.author == user


# ============================
# UPDATE / DELETE (AUTH REQUIRED)
# ============================

def test_update_requires_authentication(api_client, user):
    """Unauthenticated users cannot update an article."""
    article = Article.objects.create(
        title="Original title",
        content="Content",
        author=user
    )

    url = reverse("article-detail", args=[article.id])
    response = api_client.put(url, {"title": "Updated", "content": "Content"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_can_update_article(authenticated_client, user):
    """Authenticated users can update an article."""
    article = Article.objects.create(
        title="Original title",
        content="Content",
        author=user
    )

    url = reverse("article-detail", args=[article.id])
    response = authenticated_client.put(
        url,
        {"title": "Updated title", "content": "Updated content"}
    )

    assert response.status_code == status.HTTP_200_OK
    article.refresh_from_db()
    assert article.title == "Updated title"


def test_authenticated_user_can_delete_article(authenticated_client, user):
    """Authenticated users can delete an article."""
    article = Article.objects.create(
        title="Article to delete",
        content="Content",
        author=user
    )

    url = reverse("article-detail", args=[article.id])
    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Article.objects.count() == 0


# ============================
# SEARCH & ORDERING
# ============================

def test_article_search_by_title(api_client, user):
    """Articles can be searched using a keyword."""
    Article.objects.create(title="Python article", content="C", author=user)
    Article.objects.create(title="Django article", content="C", author=user)

    url = reverse("article-list") + "?search=Python"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Python article"


def test_article_ordering_by_title(api_client, user):
    """Articles can be ordered by title."""
    Article.objects.create(title="B Article", content="C", author=user)
    Article.objects.create(title="A Article", content="C", author=user)

    url = reverse("article-list") + "?ordering=title"
    response = api_client.get(url)

    titles = [item["title"] for item in response.data]
    assert titles == ["A Article", "B Article"]


def test_article_default_ordering_is_by_publication_date(api_client, user):
    """Articles are ordered by publication date descending by default."""
    first = Article.objects.create(
        title="Older article",
        content="C",
        author=user
    )
    second = Article.objects.create(
        title="Newer article",
        content="C",
        author=user
    )

    url = reverse("article-list")
    response = api_client.get(url)

    titles = [item["title"] for item in response.data]
    assert titles[0] == second.title
