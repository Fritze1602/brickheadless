"""Helper functions related to CMS Page handling."""

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
import cms
from content.form_renderer import extract_data
from django.utils.timezone import now, localtime


def get_page_by_slug(slug):
    """
    Returns a Page-like object from cms.py matching the given slug.
    Raises 404 if not found.
    """
    page_obj = next(
        (obj for obj in cms.__dict__.values() if getattr(obj, "slug", None) == slug),
        None,
    )
    if not page_obj:
        raise Http404("Page not found.")

    return page_obj


def save_page(content_entry, page_obj, request):
    """
    Extracts form data for the given page, assigns it to the content_entry,
    and saves the entry to the database.

    Args:
        content_entry: The ContentEntry instance to update.
        page_obj: The Page definition object from cms.py.
        request: The current Django request (with POST and FILES data).
    """
    data = extract_data(page_obj.fields, request.POST, request.FILES)
    content_entry.data = data
    content_entry.save()


def save_page_and_redirect(content_entry, page_obj, request, slug):
    save_page(content_entry, page_obj, request)
    url = reverse("cms-admin-edit-page", kwargs={"slug": slug}) + "?saved=1"
    return HttpResponseRedirect(url)


def get_saved_timestamp(request):
    if request.GET.get("saved") != "1":
        return False, "", ""

    dt = localtime(now())
    return True, dt.strftime("%H:%M"), dt.strftime("%A, %B %d")
