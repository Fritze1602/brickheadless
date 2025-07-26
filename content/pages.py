"""
BrickHeadless Content Definitions for this Project.

Define your Pages and Collections here.
This replaces manual Content-Type clicking (e.g. Strapi or Carbon Fields).
"""

from content.schema import (
    Collection,
    Page,
    Repeater,
    TextField,
    URLField,
)

homepage = Page(
    "Homepage",
    slug="homepage",
    fields=[
        TextField("Claim", "claim"),
        TextField("Slogan", "slogan"),
        URLField("LieblingsURL", "url"),
        Repeater(
            label="CTA-Texte",
            name="ctas",
            fields=[
                TextField("Text", "text"),
                URLField("URL", "url"),
            ],
        ),
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
