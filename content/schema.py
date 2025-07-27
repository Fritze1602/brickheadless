"""BrickHeadless Field-Definitions.
Carbon-Fields-Style DSL for Headless CMS in Django.
"""


class Collection:
    """
    Defines a repeatable content type (e.g. Blog, Projekte, Mitarbeiter).

    Used in brickschema/pages.py to describe a group of entries that follow the same field schema.
    Models are automatically generated via `sync_collections`, based on these fields.
    """

    def __init__(self, label, singular_label, slug, fields, unique=False):
        """
        Defines a content collection — either repeatable or singleton.

        Args:
            label (str): Human-friendly plural name (e.g. "Projects").
            singular_label (str): Singular name for UI or button text (e.g. "Project").
            slug (str): Unique system identifier (e.g. "projects", "homepage").
            fields (list): A list of field definitions (e.g. TextField, URLField, Repeater).
            unique (bool, optional):
                If True, this collection behaves like a singleton ("page").
                Only one entry will exist and can be edited, not added repeatedly.
                Default is False (multi-entry collection).
        """
        self.label = label
        self.singular_label = singular_label
        self.slug = slug
        self.fields = fields
        self.unique = unique
        self.type = "collection"


class BaseField:
    """Base Field Class for BrickHeadless."""

    def __init__(self, label, name, required=True, default=None, help_text=None):
        self.label = label
        self.name = name
        self.required = required
        self.default = default
        self.help_text = help_text


class TextField(BaseField):
    """Text Field."""

    type = "text"


class ImageField(BaseField):
    """Image Field. Muss total anders werden?"""

    type = "media"


class URLField(BaseField):
    """URL Field."""

    type = "url"


class FieldGroup:
    """Visual group of fields (purely for UI layout)."""

    def __init__(self, label, fields):
        self.label = label
        self.fields = fields
        self.type = "group"


class Repeater(BaseField):
    """Repeater Field."""

    type = "repeater"

    def __init__(self, label, name, fields, **kwargs):
        super().__init__(label, name, **kwargs)
        self.fields = fields  # ✅ Instanz-Attribut


class Page:
    """A Page with a slug and fields."""

    def __init__(self, label, slug, fields):
        self.label = label
        self.slug = slug
        self.fields = fields
