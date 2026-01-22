from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.
class Person(AbstractUser):
    created_on = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.CharField(max_length=50,
                             blank=False,
                             help_text="Required",
                             error_messages={
                                 'unique': 'A user with that email address already exists',
                                             }
                            )
    slug = models.SlugField(unique=True, blank=True)
    def __str__ (self):
        return(f"{self.first_name} {self.last_name}")
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "People"
        verbose_name = "Person"
        db_table = "people"

class BasicProfile(models.Model):
    user = models.OneToOneField(Person, on_delete=models.CASCADE)
    preferred_name = models.CharField(max_length=50, blank=True, null=True)
    work_phone = models.CharField(max_length=16, blank=True, null=True)
    cell_phone = models.CharField(max_length=16, blank=True, null=True)
    home_phone = models.CharField(max_length=16, blank=True, null=True)
    def __str__(self):
        return f"{self.user} profile"