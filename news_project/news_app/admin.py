from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Publisher, Article, Newsletter


# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Role & Subscriptions", {"fields": ("role", "reader_subscriptions_publishers", "reader_subscriptions_journalists")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("editors", "journalists")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "journalist", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("title", "body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("subject", "publisher", "journalist", "approved", "created_at")
    list_filter = ("approved", "publisher")
    search_fields = ("subject", "body")
