from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from StatusApp import signals
from StatusApp.models import UserStatus

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Downloading current users")
        users = User.objects.exclude(username="admin")
        print("Downloading current StatusApp users")
        statusUsers = UserStatus.objects.all()
        for u in users:
            found = False
            for s in statusUsers:
                if s.user == u:
                    found = True
            if not found:
                print(f"--Adding: {u}")
                signals.create_user_status(True, u, True)
        print("done")
