"""
Defines serialization for Article and related models.
"""

from rest_framework import serializers
from .models import Article, Publisher, User


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher model."""
    class Meta:
        model = Publisher
        fields = ["id", "name", "description"]


class JournalistSerializer(serializers.ModelSerializer):
    """Serializer for Journalist model."""
    class Meta:
        model = User
        fields = ["id", "username"]


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""
    publisher = PublisherSerializer(read_only=True)
    journalist = JournalistSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "body", "approved", "publisher", "journalist", "created_at"]
