"""
BrickHeadless Admin Views.

Diese Datei enthält die Views für das Redakteurs-Frontend.
Dazu gehören:
- Dashboard (Pages & Collections Übersicht)
- Seiten editieren (Page-Editor)
- Collections verwalten (List/Add/Edit für Collection-Einträge)
"""

import django
from django.utils.timezone import now, localtime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.conf import settings as django_settings
import cms
from content.models import ContentEntry
from content.model_utils import get_model_for_slug
from content.schema import Collection


from content.form_renderer import render_field, extract_data  # wichtig!


# Login
class BricksCMSLoginView(LoginView):
    """
    Custom Login-View für das BricksCMS UI (nicht Django Admin).
    """

    template_name = "bricks_admin/login.html"


# Dashboard
@login_required
def dashboard(request):
    """
    Zeigt alle Pages und Collections als Links im CMS-Admin.
    """
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


@login_required
def single_list(request):
    from content.schema import Collection
    import cms

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


@login_required
def edit_page(request, slug):
    """
    Editiert eine einzelne Page (z. B. Homepage) mit Custom Field Rendering.
    """
    # Passendes Page-Objekt aus pages.py holen
    page_obj = next(
        obj for obj in cms.__dict__.values() if getattr(obj, "slug", None) == slug
    )

    # Content aus der DB holen oder neu anlegen
    content, _ = ContentEntry.objects.get_or_create(
        slug=slug, defaults={"collection": "", "data": {}}
    )

    # Wenn gespeichert wird:
    if request.method == "POST":
        data = extract_data(page_obj.fields, request.POST, request.FILES)
        content.data = data
        content.save()
        redirect_url = (
            reverse("cms-admin-edit-page", kwargs={"slug": slug}) + "?saved=1"
        )
        return HttpResponseRedirect(redirect_url)

    # Felder fürs Template rendern
    rendered_fields = []
    saved = request.GET.get("saved") == "1"
    saved_dt = localtime(now()) if saved else None
    saved_time = saved_dt.strftime("%H:%M") if saved_dt else ""
    saved_date = (
        saved_dt.strftime("%A, %B %d") if saved_dt else ""
    )  # z. B. Thursday, July 24
    for field in page_obj.fields:
        html = render_field(field, field.name, content.data.get(field.name))
        rendered_fields.append({"label": field.label, "html": html})

    return render(
        request,
        "bricks_admin/edit_page.html",
        {
            "page": page_obj,
            "fields": rendered_fields,
            "saved": saved,
            "saved_time": saved_time,
            "saved_date": saved_date,
        },
    )


@login_required
def collection_list(request, slug):
    """
    Zeigt alle Einträge einer multiple Collection (unique=False),
    basierend auf dem generierten SQL-Modell (z. B. ProjectsEntry).
    """
    collection_obj = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )

    if not collection_obj or collection_obj.unique:
        raise Http404("Collection nicht gefunden oder ist eine Einzelseite.")

    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("Kein generiertes Modell für diese Collection gefunden.")

    entries = model_class.objects.all()

    return render(
        request,
        "bricks_admin/collection_list.html",
        {
            "collection": collection_obj,
            "entries": entries,
        },
    )


@login_required
def add_collection_entry(request, slug):
    """
    BricksCMS: Fügt einen neuen Eintrag zu einer Collection hinzu (nur für unique=False).

    - Holt das Collection-Schema aus cms.py anhand des Slugs
    - Lädt das zugehörige generierte SQL-Modell (ProjectsEntry, etc.)
    - Rendert alle definierten Felder
    - Speichert nach POST direkt als echte SQL-Instanz
    """
    # Collection-Schema aus cms.py finden
    collection = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )

    if not collection or collection.unique:
        raise Http404("Collection nicht gefunden oder ist keine multiple Collection.")

    # Zuordnung slug → generiertes Modell
    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("Kein generiertes Modell für diese Collection gefunden.")

    # Speichern bei POST
    if request.method == "POST":
        data = extract_data(collection.fields, request.POST, request.FILES)

        instance = model_class.objects.create(
            **{
                k: v
                for k, v in data.items()
                if not getattr(model_class._meta.get_field(k), "many_to_many", False)
            }
        )

        # Many-to-many Felder separat setzen
        for key, value in data.items():
            field = model_class._meta.get_field(key)
            if field.many_to_many:
                getattr(instance, key).set(value)

        return redirect("cms-admin-collection-list", slug=slug)

    # Felder rendern für das Template (inkl. Optionen für RelationFields)
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


@login_required
def edit_collection_entry(request, slug, pk):
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
                print(
                    f"✅ value for {field.name}: {ids} (type: {type(ids[0]).__name__ if ids else 'empty'})"
                )
                return [str(pk) for pk in ids]
        value = getattr(instance, field.name, None)
        print(f"🔍 Fallback value for {field.name}: {value}")
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


@login_required
def settings_page(request):
    """
    Bricks Admin: Displays system info, Django version, and registered content types.
    """

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
