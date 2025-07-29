from typing import Optional
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from content.helpers.collections import (
    get_model_and_collection,
    save_collection_instance,
)
from content.form_renderer import extract_data, render_field
from content.model_utils import get_model_for_slug


@login_required
def collection_entry(request, slug: str, pk: Optional[int] = None):
    """
    Generic view to create or edit a collection entry.

    Args:
        request: HTTP request object.
        slug (str): Slug identifying the collection.
        pk (Optional[int]): Primary key of the entry for editing, None for adding.

    Returns:
        HTTP Response rendering the form or redirecting after POST.
    """
    model_class, collection = get_model_and_collection(slug)

    if pk is not None:
        instance = get_object_or_404(model_class, pk=pk)
    else:
        instance = model_class()  # pylint: disable=not-callable

    if request.method == "POST":
        data = extract_data(collection.fields, request.POST, request.FILES)
        save_collection_instance(instance, data)
        return redirect("cms-admin-collection-edit", slug=slug, pk=instance.pk)

    def get_initial_value(field):
        if getattr(field, "type", None) == "relation" and getattr(field, "many", False):
            if pk is not None:
                rel = getattr(instance, field.name, None)
                if rel is not None and hasattr(rel, "values_list"):
                    ids = list(rel.values_list("id", flat=True))
                    return [str(pk) for pk in ids]
            return []
        return getattr(instance, field.name, "") or ""

    def get_relation_options(field):
        if getattr(field, "type", None) == "relation":
            related_model = get_model_for_slug(field.to)
            return related_model.objects.all()
        return None

    rendered_fields = []
    for field in collection.fields:
        value = get_initial_value(field)
        options = get_relation_options(field)
        html = render_field(field, field.name, value, options=options)
        rendered_fields.append(
            {
                "label": getattr(field, "label", field.name),
                "html": html,
            }
        )

    return render(
        request,
        "bricks_admin/collection_edit.html",
        {
            "collection": collection,
            "fields": rendered_fields,
            "edit_mode": pk is not None,
            "entry": instance,
        },
    )
