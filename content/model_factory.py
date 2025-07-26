"""Dynamische Django-Modellgenerierung aus BrickHeadless-Collection-Definitionen."""

from django.db import models


def camel_case(s):
    """Converts 'projects_entry' to 'ProjectsEntry'."""
    return "".join(word.capitalize() for word in s.split("_"))


FIELD_TYPE_MAP = {
    "text": lambda field: models.CharField(
        max_length=255, blank=not field.required, default=field.default or ""
    ),
    "url": lambda field: models.URLField(
        blank=not field.required, default=field.default or ""
    ),
    # Mehr Field-Types folgen später
}


def create_model_from_collection(collection):
    """
    Erstellt ein Django-Modell dynamisch aus einer Collection-Definition.
    """
    attrs = {
        "__module__": "content.models",
        "__str__": lambda self: getattr(self, "title", f"{collection.slug} entry"),
    }

    for field in collection.fields:
        if field.type in FIELD_TYPE_MAP:
            attrs[field.name] = FIELD_TYPE_MAP[field.type](field)
        else:
            raise NotImplementedError(
                f"Feldtyp '{field.type}' ist nicht implementiert."
            )

    class_name = camel_case(f"{collection.slug}_entry")

    return type(class_name, (models.Model,), attrs)
