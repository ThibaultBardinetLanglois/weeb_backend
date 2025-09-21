from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.
    
    This customizes how Contact entries appear in the Django admin interface,
    including which fields are displayed and searchable.
    """
    # Fields shown in the admin list view
    list_display = ('first_name', 'last_name', 'phone', 'email', 'message', 'created_at')
    
    # Fields searchable via the search bar in the admin
    search_fields = ('first_name', 'last_name','phone', 'email', 'created_at')