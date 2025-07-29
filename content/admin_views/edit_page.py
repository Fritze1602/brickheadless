"""Admin view for editing a single custom page (e.g. homepage)."""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from content.helpers.pages import get_page_by_slug, save_page, save_page_and_redirect
from content.helpers.ui import get_saved_timestamp
from content.form_renderer import render_fields
from content.models import ContentEntry


@login_required
def edit_page(request, slug):
    """Render and handle form submission for editing a single page."""
    page_obj = get_page_by_slug(slug)

    content, _ = ContentEntry.objects.get_or_create(
        slug=slug, defaults={"collection": "", "data": {}}
    )

    if request.method == "POST":
        return save_page_and_redirect(content, page_obj, request, slug)

    saved, saved_time, saved_date = get_saved_timestamp(request)
    rendered_fields = render_fields(page_obj, content.data)

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
