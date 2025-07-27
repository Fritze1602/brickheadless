"""
BrickHeadless CMS Admin URLs.
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from content import adminviews

urlpatterns = [
    path("login/", adminviews.BricksCMSLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", adminviews.dashboard, name="cms-admin-dashboard"),
    path(
        "cms-admin/singles/<slug:slug>/",
        adminviews.edit_page,
        name="cms-admin-edit-page",
    ),
    path(
        "collections/",
        adminviews.collection_list,
        name="cms-admin-collection-overview",
    ),
    path("singles/", adminviews.single_list, name="cms-admin-single-list"),
    path(
        "collection/<slug:slug>/",
        adminviews.collection_list,
        name="cms-admin-collection-list",
    ),
    path(
        "collection/<slug:slug>/add/",
        adminviews.add_collection_entry,
        name="cms-admin-collection-add",
    ),
    path(
        "cms-admin/collection/<slug:slug>/edit/<int:pk>/",
        adminviews.edit_collection_entry,
        name="cms-admin-collection-edit",
    ),
    path("cms-admin/settings/", adminviews.settings_page, name="cms-admin-settings"),
]
