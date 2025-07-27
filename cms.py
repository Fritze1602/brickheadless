"""
BrickHeadless Content Definitions for this Project.

Define your Pages and Collections here.
This replaces manual Content-Type clicking (e.g. Strapi or Carbon Fields).
"""

from content.schema import (
    Collection,
    Repeater,
    TextField,
    URLField,
)

homepage = Collection(
    label="Homepage",
    singular_label="Homepage",
    slug="homepage",
    unique=True,
    fields=[
        TextField(label="Claim", name="claim"),
        TextField(label="Slogan", name="slogan"),
        URLField(label="GoogleMaps", name="googleMapsUrl"),
        Repeater(
            label="CTA-Texte",
            name="ctas",
            fields=[
                TextField(label="Text", name="text"),
                URLField(label="URL", name="url"),
            ],
        ),
    ],
)

about = Collection(
    label="About Page",
    singular_label="About",
    slug="about",
    unique=True,
    fields=[
        TextField(label="Überschrift", name="headline"),
        TextField(label="Intro", name="intro"),
        TextField(label="Mission", name="mission"),
        URLField(label="Externer Link", name="external_url"),
    ],
)

projects = Collection(
    label="Projekte",
    singular_label="Projekt",
    slug="projects",
    fields=[
        TextField("Titel", "title"),
        TextField("Beschreibung", "description"),
        URLField("URL", "url"),
    ],
)

categories = Collection(
    label="Kategorien",
    singular_label="Kategorie",
    slug="categories",
    fields=[
        TextField(label="Name", name="name"),
        TextField(label="Slug", name="slug"),
    ],
)
