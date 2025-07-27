"""Auto-generated models from BrickHeadless collection definitions."""
from django.db import models

class CategoriesEntry(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.CharField(max_length=255, blank=False)

    def __str__(self) -> str:
        return str(getattr(self, 'title', 'categories entry'))

class ProjectsEntry(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=False)
    categories = models.ManyToManyField('content.CategoriesEntry', blank=True)

    def __str__(self) -> str:
        return str(getattr(self, 'title', 'projects entry'))

