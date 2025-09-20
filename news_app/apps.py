from django.apps import AppConfig
from django.db.models.signals import post_migrate


class NewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self):
        from .bootstrap import ensure_default_groups
        post_migrate.connect(ensure_default_groups, sender=self)
