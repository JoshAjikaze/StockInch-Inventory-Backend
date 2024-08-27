from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a default superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin_stock@stockinch.ng',
                name='Admin User',
                password='kunleADMIN@123'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created default superuser'))
        else:
            self.stdout.write(self.style.WARNING('Default superuser already exists'))
