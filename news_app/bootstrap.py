"""
Contains logic to initialize roles, groups, or default data.
"""

from django.contrib.auth.models import Group


def ensure_default_groups(sender, **kwargs):
    # Ensure that default groups (Reader, Editor, Journalist) exist.
    roles = ["Reader", "Editor", "Journalist"]
    for role in roles:
        group, created = Group.objects.get_or_create(name=role)
        if created:
            print(f"Created group: {role}")
