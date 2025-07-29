"""Admin view for displaying system and environment information."""

import django
from django.conf import settings as django_settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import cms
from content.schema import Collection


@login_required
def settings_page(request):
    """Render the settings page with system and content metadata."""
    collections = [obj for obj in cms.__dict__.values() if isinstance(obj, Collection)]

    return render(
        request,
        "bricks_admin/settings.html",
        {
            "collections": collections,
            "django_version": django.get_version(),
            "vite_dev": getattr(django_settings, "VITE_DEV", False),
        },
    )
