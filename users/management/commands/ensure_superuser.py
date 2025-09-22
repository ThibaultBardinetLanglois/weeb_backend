from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Ensure a default superuser exists (idempotent)"

    def handle(self, *args, **options):
        User = get_user_model()

        email = "admin@gmail.com"
        first_name = "admin"
        last_name = "admin"
        password = "admin"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} created."))
        else:
            self.stdout.write(f"Superuser {email} already exists.")
