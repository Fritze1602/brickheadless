"""Automatisch generierte Modelle aus BrickHeadless Collection-Definitionen."""

from django.db import models


class CategoriesEntry(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return getattr(self, "title", "categories entry")


class ProjectsEntry(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=False)

    def __str__(self):
        return getattr(self, "title", "projects entry")
