"""
BrickHeadless API Views.

Stellt die Headless JSON-API bereit für:
- Einzelne Seiten (page_detail)
- Collections als Liste (collection_list)
"""

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from content.models import ContentEntry
from content import generated_models


@api_view(["GET"])
def page_detail(_request, slug):
    """
    Gibt eine einzelne Seite als JSON zurück.

    Args:
        _request: Unused request object (required for Django view signature)
        slug: Der Slug der Seite
    """
    try:
        entry = ContentEntry.objects.get(slug=slug)
        return Response(entry.data)
    except ObjectDoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(["GET"])
def dynamic_collection_list(_request, slug):
    """
    Returns all entries for a collection.

    Collection must be defined via `Collection(...)` in `cms.py`.
    """
    model_name = f"{slug.capitalize()}Entry"
    model = getattr(generated_models, model_name, None)
    if not model:
        raise Http404(f"No collection model found for slug '{slug}'")

    entries = model.objects.all()
    return Response(
        [
            {field.name: getattr(entry, field.name) for field in entry._meta.fields}
            for entry in entries
        ]
    )
