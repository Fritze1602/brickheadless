"""Admin view for listing all singleton (unique) pages."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import cms
from content.schema import Collection


@login_required
def single_list(request):
    """Render a list of all singleton collections (unique=True)."""
    singles = []

    for obj in cms.__dict__.values():
        if isinstance(obj, Collection) and getattr(obj, "unique", False):
            singles.append(obj)

    return render(
        request,
        "bricks_admin/single_list.html",
        {
            "singleton_collections": singles,
        },
    )
