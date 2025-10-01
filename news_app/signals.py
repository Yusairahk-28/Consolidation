"""
Defines post-save or other signals for models.
"""
                                  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import requests

from .models import Article


def post_to_x(text: str):
    if not getattr(settings, "X_POSTING_ENABLED", False):
        return
    token = getattr(settings, "X_BEARER_TOKEN", "")
    if not token:
        return
    try:
        requests.post(
            "https://api.twitter.com/2/tweets",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": text},
            timeout=10
        )
    except Exception:
        pass


@receiver(post_save, sender=Article)
"""Sends signal to notify when article is published."""
def article_approval_handler(sender, instance: Article, created, **kwargs):
    if instance.approved:
        subscribers = set()
        if instance.publisher:
            subscribers.update(instance.publisher.subscribed_readers.all())
        subscribers.update(instance.journalist.reader_followers.all())

        # Exetends to send emails.
        subject = f"New Article: {instance.title}"
        body = instance.body[:500] + ("..." if len(instance.body) > 500 else "")
        from_email = settings.DEFAULT_FROM_EMAIL
        for reader in subscribers:
            if reader.email:
                try:
                    send_mail(subject, body, from_email, [reader.email], fail_silently=True)
                except Exception:
                    pass
        post_to_x(f"New article published: {instance.title}")

