"""
Management command: Generates Django models from Bricks Collection definitions in cms.py.
"""

import os
from django.core.management.base import BaseCommand
from content.management.definition_loader import load_definitions_from_module

GENERATED_FILE = os.path.join("content", "generated_models.py")


class Command(BaseCommand):
    """
    CLI command to sync Bricks Collection definitions into generated Django models.

    Only non-unique collections (repeatable content) are written out.
    Singleton pages (unique=True) are ignored — handled via ContentEntry.
    """

    help = "Syncs Bricks Collections with Django model definitions (excludes singleton pages)."

    def handle(self, *args, **options):
        _, collections = load_definitions_from_module("cms")

        with open(GENERATED_FILE, "w", encoding="utf-8") as f:
            f.write(
                '"""Auto-generated models from BrickHeadless collection definitions."""\n'
            )
            f.write("from django.db import models\n\n")

            for collection in collections:
                # 🛑 SKIP pages (singleton content)
                if getattr(collection, "unique", False):
                    continue

                class_name = (
                    "".join(word.capitalize() for word in collection.slug.split("_"))
                    + "Entry"
                )
                f.write(f"class {class_name}(models.Model):\n")

                if not collection.fields:
                    f.write("    pass\n")

                for field in collection.fields:
                    if field.type == "text":
                        f.write(
                            f"    {field.name} = models.CharField(max_length=255, blank={not field.required})\n"
                        )
                    elif field.type == "url":
                        f.write(
                            f"    {field.name} = models.URLField(blank={not field.required})\n"
                        )
                    elif field.type == "relation":
                        target_model = (
                            "".join(word.capitalize() for word in field.to.split("_"))
                            + "Entry"
                        )

                        if getattr(field, "many", False):
                            f.write(
                                f"    {field.name} = models.ManyToManyField('content.{target_model}', blank=True)\n"
                            )
                        else:
                            f.write(
                                f"    {field.name} = models.ForeignKey('content.{target_model}', null=True, blank=True, on_delete=models.SET_NULL)\n"
                            )
                    else:
                        f.write(
                            f"    # {field.name}: unsupported field type '{field.type}'\n"
                        )

                f.write("\n    def __str__(self) -> str:\n")
                f.write(
                    f"        return str(getattr(self, 'title', '{collection.slug} entry'))\n\n"
                )

        self.stdout.write("✅ Collections synced → content/generated_models.py")
