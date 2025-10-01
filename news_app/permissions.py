"""
permissions.py - Custom DRF permissions for news_app.
"""

from rest_framework.permissions import BasePermission


class IsReader(BasePermission):
    """Only Readers can modify content."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Reader").exists()


class IsEditor(BasePermission):
    """Only Editors can modify content."""
    def has_permission(self, request, view):
        # Check if user has editor role.
        return request.user.is_authenticated and request.user.groups.filter(name="Editor").exists()


class IsJournalist(BasePermission):
    """Only Journalists can modify content."""
    def has_permission(self, request, view):
        """Check if user has journalist role."""
        return request.user.is_authenticated and request.user.groups.filter(name="Journalist").exists()
