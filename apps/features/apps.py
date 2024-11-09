from django.apps import AppConfig


class FeaturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features'

    def ready(self) -> None:
        from features import signals
        return super().ready()
