from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from StatusApp import signals
from StatusApp.models import UserStatus, Status

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        lock_status = UserStatus.objects.filter(lock_status=False)
        lock_notes = UserStatus.objects.filter(lock_notes=False)
        unknown_status = Status.objects.get(name="UNKNOWN")
        for u in lock_status:
            print(f"Setting {u} status to {unknown_status}")
            u.status = unknown_status
            u.save()
        for u in lock_notes:
            print(f"Clearing notes for {u}")
            u.notes = ""
            u.save()
