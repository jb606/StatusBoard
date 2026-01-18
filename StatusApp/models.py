from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

BOOTSTRAP_BUTTON_CHOICES = (
    ("btn-primary", "Primary"),
    ("btn-secondary", "Secondary"),
    ("btn-success", "Success"),
    ("btn-danger", "Danger"),
    ("btn-warning", "Warning"),
    ("btn-info", "Infomation"),
    ("btn-light", "Light"),
    ("btn-dark", "Dark"),
    ("btn-link", "Link"),
)

User = get_user_model()


class Status(models.Model):
    name = models.CharField(max_length=50)
    css = models.CharField(
        max_length=15,
        choices=BOOTSTRAP_BUTTON_CHOICES,
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Status"
        verbose_name = "Status"
        db_table = "status"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class UserStatus(models.Model):
    class Meta:
        verbose_name_plural = "UserStatus"
        verbose_name = "UserStatus"
        db_table = "User_status"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="status")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    lock_status = models.BooleanField(default=False)
    lock_notes = models.BooleanField(default=False)
    notes = models.CharField(max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_%(class)s_set",
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        user = kwargs.pop("User", None)
        if user:
            self.updated_by = user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(UserStatus, related_name="member_of", blank=True)
    mods = models.ManyToManyField(UserStatus, related_name="moderating", blank=True)
    slug = models.SlugField(unique=True, blank=True)
    external_sync = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
