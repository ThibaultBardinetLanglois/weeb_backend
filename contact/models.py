from django.db import models

class Contact(models.Model):
    """
    Model representing a contact form submission.

    Stores basic contact information and the message sent by a user
    via a contact form, with the timestamp of submission.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField(max_length=999)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the contact instance.
        Useful for displaying entries in the Django admin.
        """
        return f"{self.first_name} {self.last_name}"
