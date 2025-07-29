"""Admin view for listing entries of a multiple (non-unique) collection."""

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
import cms
from content.schema import Collection
from content.model_utils import get_model_for_slug


@login_required
def collection_list(request, slug):
    """Render the entry list view for a non-unique collection."""
    collection_obj = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )

    if not collection_obj or collection_obj.unique:
        raise Http404("Collection not found or is a singleton.")

    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("No model found for this collection.")

    entries = model_class.objects.all()

    return render(
        request,
        "bricks_admin/collection_list.html",
        {
            "collection": collection_obj,
            "entries": entries,
        },
    )
