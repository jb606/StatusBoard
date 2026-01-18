from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import UserStatus, Status


@receiver(post_save, sender=get_user_model())
def create_user_status(sender, instance, created, **kwargs):
    if created:
        status = Status.objects.get(name="UNKNOWN")
        new_userstatus = UserStatus(user=instance, status=status)
        new_userstatus.save()
