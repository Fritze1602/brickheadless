"""
BrickHeadless CMS Admin URLs.
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from content import adminviews

urlpatterns = [
    path("cms-admin/login/", adminviews.BricksCMSLoginView.as_view(), name="login"),
    path("cms-admin/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", adminviews.dashboard, name="cms-admin-dashboard"),
    path("page/<slug:slug>/", adminviews.edit_page, name="cms-admin-edit-page"),
    path(
        "collection/<slug:slug>/",
        adminviews.collection_list,
        name="cms-admin-collection-list",
    ),
    path(
        "collection/<slug:slug>/add/",
        adminviews.collection_add,
        name="cms-admin-collection-add",
    ),
    path(
        "collection/<slug:slug>/<int:pk>/edit/",
        adminviews.collection_edit,
        name="cms-admin-collection-edit",
    ),
]
