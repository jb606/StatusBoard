from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group


def create_default_statuses(apps, schema_editor):
    Status = apps.get_model("StatusApp", "Status")

    defaults = [
        {
            "slug": "unknown",
            "name": "UNKNOWN",
            "css": "btn-secondary",
        },
        {
            "slug": "in",
            "name": "IN",
            "css": "btn-success",
        },
        {
            "slug": "out",
            "name": "OUT",
            "css": "btn-danger",
        },
        {
            "slug": "gftd",
            "name": "GFTD",
            "css": "btn-warning",
        },
        {
            "slug": "al",
            "name": "A/L",
            "css": "btn-warning",
        },
    ]

    for data in defaults:
        Status.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "name": data["name"],
                "css": data["css"],
            },
        )


def remove_default_statuses(apps, schema_editor):
    Status = apps.get_model("StatusApp", "Status")

    Status.objects.filter(slug__in=["unknown", "in", "out"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("StatusApp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_default_statuses,
            reverse_code=remove_default_statuses,
        ),
    ]
