"""
BrickHeadless Content API URLs.
"""

from django.urls import path
from content import api_views  # Legen wir gleich an

urlpatterns = [
    path("<slug:slug>/", api_views.page_detail, name="api-page-detail"),
    path("collections/<slug:slug>/", api_views.dynamic_collection_list),
]
