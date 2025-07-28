"""Dashboard and single-page listing views for the BricksCMS admin interface."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import cms
from content.schema import Collection


@login_required
def dashboard(request):
    """Render the main admin dashboard with pages and collections."""
    singleton_collections = []
    multi_collections = []

    for obj in cms.__dict__.values():
        if isinstance(obj, Collection):
            if obj.unique:
                singleton_collections.append(obj)
            else:
                multi_collections.append(obj)

    return render(
        request,
        "bricks_admin/dashboard.html",
        {
            "singleton_collections": singleton_collections,
            "multi_collections": multi_collections,
        },
    )
