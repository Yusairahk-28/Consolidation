"""
Defines User, Article, Publisher, Roles and Newsletter models.
"""


from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings


class Roles(models.TextChoices):
    # Custom role field.
    READER = "reader", "Reader"
    EDITOR = "editor", "Editor"
    JOURNALIST = "journalist", "Journalist"


class User(AbstractUser):
    # Custom user model.
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.READER)

    reader_subscriptions_publishers = models.ManyToManyField(
        "Publisher", blank=True, related_name="subscribed_readers"
    )
    reader_subscriptions_journalists = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="reader_followers"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        role_to_group = {
            Roles.READER: "Reader",
            Roles.EDITOR: "Editor",
            Roles.JOURNALIST: "Journalist",
        }
        group_name = role_to_group.get(self.role)
        if group_name:
            try:
                group, _ = Group.objects.get_or_create(name=group_name)
                for g in Group.objects.filter(name__in=role_to_group.values()):
                    if self.groups.filter(id=g.id).exists() and g.name != group_name:
                        self.groups.remove(g)
                self.groups.add(group)
            except Exception:
                pass


class Publisher(models.Model):
    # Model representing a news publisher.
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="editor_publishers")
    journalists = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="journalist_publishers")
    def __str__(self): return self.name


class Article(models.Model):
    # Model representing a news Article.
    title = models.CharField(max_length=255)
    body = models.TextField()
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles")
    journalist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_articles")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.title


class Newsletter(models.Model):
    # Model representing a Newsletter.
    subject = models.CharField(max_length=255)
    body = models.TextField()
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.SET_NULL, related_name="newsletters")
    journalist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_newsletters")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.subject



