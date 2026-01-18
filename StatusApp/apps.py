from django.apps import AppConfig


class StatusappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "StatusApp"

    def ready(self):
        import StatusApp.signals
        import StatusApp.menu
