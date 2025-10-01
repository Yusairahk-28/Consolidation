from django.apps import AppConfig
from django.db.models.signals import post_migrate


class NewsAppConfig(AppConfig):
    """Configuration class for the news_app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self):
        """Connects when app is ready."""
        from .bootstrap import ensure_default_groups
        post_migrate.connect(ensure_default_groups, sender=self)
