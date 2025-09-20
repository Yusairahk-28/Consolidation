from rest_framework import serializers
from .models import Article, Publisher, User


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "description"]


class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ArticleSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    journalist = JournalistSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "body", "approved", "publisher", "journalist", "created_at"]
