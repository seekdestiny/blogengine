from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="jeffqian").exists():
            User.objects.create_superuser("jeffqian", "jifeiqian@gmail.com", "Qx6y123Y")
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
