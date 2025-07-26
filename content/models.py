"""Datenmodelle für BrickHeadless: Pages + generierte Collections."""

import sys
from django.db import models
from . import generated_models


# --- 📄 Pages-Modell ------------------------------------------


class ContentEntry(models.Model):
    """
    Einfache Seiten wie Homepage, Kontakt, Impressum etc.

    Speichert:
    - slug: z. B. 'homepage'
    - collection: z. B. 'homepage'
    - data: JSON mit allen Feldern
    """

    slug = models.SlugField(unique=True)
    collection = models.CharField(max_length=100, null=True, blank=True)
    data = models.JSONField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.collection}: {self.slug}"


# --- 📦 Collections: Generierte Modelle -----------------------

# Alle Klassen aus generated_models übernehmen, wenn sie echte Models sind
_current = sys.modules[__name__]

for name in dir(generated_models):
    obj = getattr(generated_models, name)
    if isinstance(obj, type) and issubclass(obj, models.Model):
        setattr(_current, name, obj)
