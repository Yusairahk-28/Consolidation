"""
Defines Django REST Framework views for Article  Publisher and Journalist management.
"""

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Article, Publisher, User
from .serializers import ArticleSerializer, PublisherSerializer, JournalistSerializer


class IsAuthenticatedReader(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.filter(approved=True).select_related("publisher", "journalist").order_by("-created_at")
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedReader]

    @action(detail=False, methods=["get"], url_path="for-subscriber/(?P<user_id>[^/.]+)")
    def for_subscriber(self, request, user_id=None):
        user = get_object_or_404(User, pk=user_id)
        pubs = user.reader_subscriptions_publishers.all()
        journos = user.reader_subscriptions_journalists.all()
        qs = (Article.objects.filter(approved=True, publisher__in=pubs) |
              Article.objects.filter(approved=True, journalist__in=journos)).distinct().order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publisher.objects.all().order_by("name")
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticatedReader]


class JournalistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(role="journalist").order_by("username")
    serializer_class = JournalistSerializer
    permission_classes = [IsAuthenticatedReader]

