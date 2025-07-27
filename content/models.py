"""Datenmodelle für BrickHeadless: Pages + generierte Collections."""

import sys
import shortuuid
from django.db import models
from . import generated_models


# --- 📄 Pages-Modell ------------------------------------------


class ContentEntry(models.Model):
    """
    A single page (e.g. homepage, about, imprint).

    Each page is stored as structured JSON under a unique slug.
    """

    id = models.AutoField(primary_key=True)
    bricks_id = models.CharField(
        max_length=22,
        default=shortuuid.uuid(),
        # unique=True,
        editable=False,
        null=True,
    )

    slug = models.SlugField(unique=True)
    collection = models.CharField(max_length=100, null=True, blank=True)
    data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.collection}: {self.slug}"


# --- 📦 Collections: Generierte Modelle -----------------------

# Alle Klassen aus generated_models übernehmen, wenn sie echte Models sind
_current = sys.modules[__name__]

for name in dir(generated_models):
    obj = getattr(generated_models, name)
    if isinstance(obj, type) and issubclass(obj, models.Model):
        setattr(_current, name, obj)
