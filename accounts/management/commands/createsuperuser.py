from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Create a superuser with a custom role field'

    def handle(self, *args, **options):
        # Set the role to 'admin' for superusers
        options['role'] = 'admin'
        return super().handle(*args, **options)