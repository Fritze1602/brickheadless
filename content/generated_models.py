"""Automatisch generierte Modelle aus BrickHeadless Collection-Definitionen."""
from django.db import models

class ProjectsEntry(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    url = models.URLField(blank=False)

    def __str__(self):
        return getattr(self, 'title', 'projects entry')

