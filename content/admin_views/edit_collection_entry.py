"""Admin view for editing an existing entry in a non-unique collection."""

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import cms
from content.schema import Collection
from content.model_utils import get_model_for_slug
from content.form_renderer import render_field, extract_data


@login_required
def edit_collection_entry(request, slug, pk):
    """Render form and handle submission for editing a collection entry."""
    collection = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )
    if not collection or collection.unique:
        raise Http404("Unknown or invalid collection.")

    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("No model found for this collection.")

    instance = get_object_or_404(model_class, pk=pk)

    if request.method == "POST":
        data = extract_data(collection.fields, request.POST, request.FILES)
        for key, value in data.items():
            field = instance._meta.get_field(key)
            if field.many_to_many:
                getattr(instance, key).set(value)
            else:
                setattr(instance, key, value)
        instance.save()
        redirect_url = (
            reverse("cms-admin-collection-edit", kwargs={"slug": slug, "pk": pk})
            + "?saved=1"
        )
        return HttpResponseRedirect(redirect_url)

    def get_initial_value(field):
        if field.type == "relation" and field.many:
            rel = getattr(instance, field.name, None)
            if rel is not None:
                ids = list(rel.values_list("id", flat=True))
                return [str(pk) for pk in ids]
        value = getattr(instance, field.name, None)
        return value

    def get_relation_options(field):
        if field.type == "relation":
            related_model = get_model_for_slug(field.to)
            return related_model.objects.all()
        return None

    rendered_fields = []
    for field in collection.fields:
        value = get_initial_value(field)
        options = get_relation_options(field)
        rendered = render_field(field, field.name, value, options=options)
        rendered_fields.append(
            {
                "label": field.label,
                "html": rendered,
            }
        )

    return render(
        request,
        "bricks_admin/collection_edit.html",
        {
            "collection": collection,
            "fields": rendered_fields,
            "edit_mode": True,
            "entry": instance,
        },
    )
