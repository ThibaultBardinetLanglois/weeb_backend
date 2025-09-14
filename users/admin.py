from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active"]
    search_fields = ["email", "first_name", "last_name"]

    # Définit l’organisation du formulaire lors de l'édition dans l'admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Informations personnelles"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Dates importantes"), {"fields": ("last_login", "date_joined")}),
    )

    # Définit les champs affichés dans le formulaire de création d’un nouvel utilisateur
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2", "is_active", "is_staff"),
        }),
    )
