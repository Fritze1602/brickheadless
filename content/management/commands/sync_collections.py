"""Management-Command: Generiert Django-Modelle aus Collection-Definitionen in pages.py."""

import os
from django.core.management.base import BaseCommand
from content.management.definition_loader import load_definitions_from_module

GENERATED_FILE = os.path.join("content", "generated_models.py")


class Command(BaseCommand):
    """CLI-Command zum Synchronisieren und Generieren von content/generated_models.py."""

    help = "Synchronisiert Collection-Definitionen mit generierten Django-Modellen."

    def handle(self, *args, **options):
        _, collections = load_definitions_from_module("cms")
        with open(GENERATED_FILE, "w", encoding="utf-8") as f:
            f.write(
                '"""Automatisch generierte Modelle aus BrickHeadless Collection-Definitionen."""\n'
            )
            f.write("from django.db import models\n\n")

            for collection in collections:
                class_name = (
                    "".join(word.capitalize() for word in collection.slug.split("_"))
                    + "Entry"
                )
                f.write(f"class {class_name}(models.Model):\n")

                for field in collection.fields:
                    if field.type == "text":
                        f.write(
                            f"    {field.name} = models.CharField(max_length=255, blank={not field.required})\n"
                        )
                    elif field.type == "url":
                        f.write(
                            f"    {field.name} = models.URLField(blank={not field.required})\n"
                        )
                    else:
                        f.write(
                            f"    # {field.name}: unsupported field type '{field.type}'\n"
                        )

                f.write("\n    def __str__(self) -> str:\n")
                f.write(
                    f"        return str(getattr(self, 'title', '{collection.slug} entry'))\n\n"
                )

        self.stdout.write(
            "✅ Collection-Modelle synchronisiert → content/generated_models.py"
        )
