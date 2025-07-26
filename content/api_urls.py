"""
BrickHeadless Content API URLs.
"""

from django.urls import path
from content import api_views  # Legen wir gleich an

urlpatterns = [
    path('<slug:slug>/', api_views.page_detail, name='api-page-detail'),
    path('collection/<slug:slug>/', api_views.collection_list, name='api-collection-list'),
]
