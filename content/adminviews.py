"""
BrickHeadless Admin Views.

Diese Datei enthält die Views für das Redakteurs-Frontend.
Dazu gehören:
- Dashboard (Pages & Collections Übersicht)
- Seiten editieren (Page-Editor)
- Collections verwalten (List/Add/Edit für Collection-Einträge)
"""

from django.utils.timezone import now, localtime
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from content import pages
from content.models import ContentEntry

from content.schema import Page, Collection


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
    pages_list = []
    collections_list = []

    for obj in pages.__dict__.values():
        if isinstance(obj, Page):
            pages_list.append(obj)
        elif isinstance(obj, Collection):
            collections_list.append(obj)

    return render(
        request,
        "bricks_admin/dashboard.html",
        {
            "pages": pages_list,
            "collections": collections_list,
        },
    )


@login_required
def edit_page(request, slug):
    """
    Editiert eine einzelne Page (z. B. Homepage) mit Custom Field Rendering.
    """
    # Passendes Page-Objekt aus pages.py holen
    page_obj = next(
        obj for obj in pages.__dict__.values() if getattr(obj, "slug", None) == slug
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
    Zeigt eine Liste von Collection-Einträgen.
    """
    entries = ContentEntry.objects.filter(collection=slug)
    collection_obj = next(
        obj for obj in pages.__dict__.values() if getattr(obj, "slug", None) == slug
    )

    return render(
        request,
        "admin/collection_list.html",
        {"entries": entries, "collection": collection_obj},
    )


@login_required
def collection_add(request, slug):
    """
    Fügt einen neuen Collection-Eintrag hinzu.
    """
    # Das Collection-Schema aus pages.py holen
    collection_obj = next(
        obj for obj in pages.__dict__.values() if getattr(obj, "slug", None) == slug
    )

    # Beim Speichern: Daten extrahieren & speichern
    if request.method == "POST":
        data = extract_data(collection_obj.fields, request.POST, request.FILES)
        ContentEntry.objects.create(
            slug="", collection=slug, data=data  # bleibt leer bei Collections
        )
        return redirect("cms-admin-collection-list", slug=slug)

    # Felder rendern
    rendered_fields = []
    for field in collection_obj.fields:
        html = render_field(field, field.name, None)
        rendered_fields.append({"label": field.label, "html": html})

    return render(
        request,
        "bricks_admin/collection_form.html",
        {"fields": rendered_fields, "collection": collection_obj},
    )


@login_required
def collection_edit(request, slug, pk):
    """
    Bearbeitet einen Collection-Eintrag.
    """
    collection_obj = next(
        obj for obj in pages.__dict__.values() if getattr(obj, "slug", None) == slug
    )
    entry = get_object_or_404(ContentEntry, pk=pk)

    if request.method == "POST" and form.is_valid():
        entry.data = form.cleaned_data
        entry.save()
        return redirect("cms-admin-collection-list", slug=slug)

    return render(
        request,
        "admin/collection_form.html",
        {"form": form, "collection": collection_obj},
    )
