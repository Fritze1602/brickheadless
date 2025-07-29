"""BrickHeadless CMS Admin URLs."""

from django.urls import path
from django.contrib.auth.views import LogoutView
from content import admin_views

urlpatterns = [
    path("login/", admin_views.BricksCMSLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", admin_views.dashboard, name="cms-admin-dashboard"),
    path(
        "cms-admin/singles/<slug:slug>/",
        admin_views.edit_page,
        name="cms-admin-edit-page",
    ),
    path(
        "collections/",
        admin_views.collection_list,
        name="cms-admin-collection-overview",
    ),
    path("singles/", admin_views.single_list, name="cms-admin-single-list"),
    path(
        "collection/<slug:slug>/",
        admin_views.collection_list,
        name="cms-admin-collection-list",
    ),
    # ADD
    path(
        "cms-admin/collection/<slug:slug>/add/",
        admin_views.collection_entry,
        name="cms-admin-collection-add",
    ),
    # EDIT
    path(
        "cms-admin/collection/<slug:slug>/<int:pk>/",
        admin_views.collection_entry,
        name="cms-admin-collection-edit",
    ),
    path("cms-admin/settings/", admin_views.settings_page, name="cms-admin-settings"),
]
