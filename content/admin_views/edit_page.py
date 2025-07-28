"""Admin view for editing a single custom page (e.g. homepage)."""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now, localtime
import cms
from content.models import ContentEntry
from content.form_renderer import render_field, extract_data


@login_required
def edit_page(request, slug):
    """Render and handle form submission for editing a single page."""
    # Get matching page object from cms.py
    page_obj = next(
        obj for obj in cms.__dict__.values() if getattr(obj, "slug", None) == slug
    )

    # Load or create content from the database
    content, _ = ContentEntry.objects.get_or_create(
        slug=slug, defaults={"collection": "", "data": {}}
    )

    if request.method == "POST":
        data = extract_data(page_obj.fields, request.POST, request.FILES)
        content.data = data
        content.save()
        redirect_url = (
            reverse("cms-admin-edit-page", kwargs={"slug": slug}) + "?saved=1"
        )
        return HttpResponseRedirect(redirect_url)

    # Render fields for the template
    rendered_fields = []
    saved = request.GET.get("saved") == "1"
    saved_dt = localtime(now()) if saved else None
    saved_time = saved_dt.strftime("%H:%M") if saved_dt else ""
    saved_date = saved_dt.strftime("%A, %B %d") if saved_dt else ""

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
