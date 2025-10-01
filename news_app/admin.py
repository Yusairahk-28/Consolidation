"""
Registers models with the Django admin site so they can be managed via the admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Publisher, Article, Newsletter


@admin.register(User)
"""Admin configuration for the custom User model."""
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Role & Subscriptions", {"fields": ("role", "reader_subscriptions_publishers", "reader_subscriptions_journalists")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")


@admin.register(Publisher)
"""Admin configuration for the Publisher model."""
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("editors", "journalists")


@admin.register(Article)
"""Admin configuration for the Article model."""
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "journalist", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("title", "body")


@admin.register(Newsletter)
"""Admin configuration for the Newsletter model."""
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("subject", "publisher", "journalist", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("subject", "body")
