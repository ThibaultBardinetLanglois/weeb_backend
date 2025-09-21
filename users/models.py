from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    Provides helper methods for creating regular users and superusers.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with all permissions enabled.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model based on AbstractBaseUser, identified by email instead of username.
    """

    username = None  # on supprime le champ username
    email = models.EmailField(unique=True)  # email unique obligatoire
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=False)   # compte validé par admin
    is_staff = models.BooleanField(default=False)    # accès admin site

    objects = CustomUserManager()

    USERNAME_FIELD = "email"   # identifiant principal
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        """Return the email as the string representation of the user."""
        return self.email
