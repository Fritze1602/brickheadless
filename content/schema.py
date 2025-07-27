"""
BrickHeadless Field-Definitions.
Carbon-Fields-Style DSL for Headless CMS in Django.
"""


class BaseField:
    """
    Base class for all schema fields.

    Used to define the structure of content types
    (e.g. TextField, URLField, RelationField, etc.)
    """

    def __init__(self, label, name, required=True, default=None, help_text=None):
        """
        Args:
            label (str): Human-readable label (used in admin UI).
            name (str): Internal name (used as key in JSON/API/model).
            required (bool): Whether this field must be filled.
            default (Any): Optional default value.
            help_text (str, optional): Additional info for UI or documentation.
        """
        self.label = label
        self.name = name
        self.required = required
        self.default = default
        self.help_text = help_text


class TextField(BaseField):
    """Simple text field (single-line)."""

    type = "text"


class URLField(BaseField):
    """A URL field for external or internal links."""

    type = "url"


class ImageField(BaseField):
    """
    Image/media field.

    Should store: URL, alt-text, dimensions, optionally crop/variant info.
    """

    type = "media"


class Repeater(BaseField):
    """
    A repeatable group of fields (array of items).

    Example:
        - Gallery images
        - List of team members
    """

    type = "repeater"

    def __init__(self, label, name, fields, **kwargs):
        """
        Args:
            fields (list): A list of sub-fields inside this repeater.
        """
        super().__init__(label, name, **kwargs)
        self.fields = fields


class RelationField(BaseField):
    """
    A relation to another collection (1:n or n:n).

    Used to define references between entries.
    """

    type = "relation"

    def __init__(self, label, name, to, many=False, **kwargs):
        """
        Args:
            to (str): Target collection slug (e.g. "categories").
            many (bool): True for ManyToMany, False for ForeignKey.
        """
        super().__init__(label, name, **kwargs)
        self.to = to
        self.many = many


class FieldGroup:
    """
    A visual grouping of fields (used for admin UI layout only).

    Does not affect database or API structure.
    """

    def __init__(self, label, fields):
        """
        Args:
            label (str): Group headline for UI.
            fields (list): List of BaseField objects.
        """
        self.label = label
        self.fields = fields
        self.type = "group"


class Page:
    """
    Defines a single, unique content entry (singleton).

    Examples:
        - Homepage
        - About
        - Imprint

    Only one instance will exist for this schema.
    """

    def __init__(self, label, slug, fields):
        """
        Args:
            label (str): Human-friendly name (e.g. "About Page").
            slug (str): Unique identifier (e.g. "about").
            fields (list): List of BaseField instances.
        """
        self.label = label
        self.slug = slug
        self.fields = fields


class Collection:
    """
    Defines a repeatable content type (e.g. Blogposts, Projekte, Team).

    Can be used as regular entries (multi) or as singleton ("page mode").
    """

    def __init__(self, label, singular_label, slug, fields, unique=False):
        """
        Args:
            label (str): Plural name (e.g. "Projects").
            singular_label (str): Singular name (e.g. "Project").
            slug (str): Identifier for model, admin, and API (e.g. "projects").
            fields (list): List of BaseField instances.
            unique (bool): If True, acts like a singleton Page.
        """
        self.label = label
        self.singular_label = singular_label
        self.slug = slug
        self.fields = fields
        self.unique = unique
        self.type = "collection"
