"""
api_urls.py - API URL routing for news_app.

Defines REST API routes for the app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, PublisherViewSet, JournalistViewSet

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"publishers", PublisherViewSet, basename="publisher")
router.register(r"journalists", JournalistViewSet, basename="journalist")

urlpatterns = [
    path("", include(router.urls)),
]

