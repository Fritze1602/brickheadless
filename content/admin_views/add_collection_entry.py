"""Admin view for creating a new entry in a non-unique collection."""

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
import cms
from content.schema import Collection
from content.model_utils import get_model_for_slug
from content.form_renderer import render_field, extract_data


@login_required
def add_collection_entry(request, slug):
    """Render form and handle submission for adding a new collection entry."""
    collection = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )

    if not collection or collection.unique:
        raise Http404("Collection not found or is not a multiple collection.")

    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("No model found for this collection.")

    if request.method == "POST":
        data = extract_data(collection.fields, request.POST, request.FILES)

        instance = model_class.objects.create(
            **{
                k: v
                for k, v in data.items()
                if not getattr(model_class._meta.get_field(k), "many_to_many", False)
            }
        )

        for key, value in data.items():
            field = model_class._meta.get_field(key)
            if field.many_to_many:
                getattr(instance, key).set(value)

        return redirect("cms-admin-collection-list", slug=slug)

    rendered_fields = []
    for field in collection.fields:
        value = None
        options = None

        if field.type == "relation":
            related_model = get_model_for_slug(field.to)
            if related_model:
                options = related_model.objects.all()

        rendered_fields.append(
            {
                "label": field.label,
                "html": render_field(field, field.name, value, options=options),
            }
        )

    return render(
        request,
        "bricks_admin/collection_edit.html",
        {
            "collection": collection,
            "fields": rendered_fields,
            "edit_mode": True,
        },
    )
