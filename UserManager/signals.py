from . import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.BasicProfile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_profile(sender, instance, **kwargs):
    instance.basicprofile.save()