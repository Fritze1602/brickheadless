"""
BrickHeadless API Views.

Stellt die Headless JSON-API bereit für:
- Einzelne Seiten (page_detail)
- Collections als Liste (collection_list)
"""

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from content.models import ContentEntry


@api_view(['GET'])
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



@api_view(['GET'])
def collection_list(_request, slug):
    """
    Gibt eine Collection als JSON-Liste zurück.
    """
    entries = ContentEntry.objects.filter(collection=slug)
    return Response([entry.data for entry in entries])
