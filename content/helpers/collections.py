# content/helpers/collections.py

from typing import Tuple, Type
from django.http import Http404
from django.db.models import Model
import cms
from content.schema import Collection
from content.model_utils import get_model_for_slug


def get_collection_by_slug(slug):
    """Finde eine Collection anhand ihres Slugs."""
    collection = next(
        (
            obj
            for obj in cms.__dict__.values()
            if isinstance(obj, Collection) and obj.slug == slug
        ),
        None,
    )
    if not collection:
        raise Http404(f"Collection '{slug}' nicht gefunden.")
    return collection


def get_model_and_collection(
    slug: str, require_non_unique: bool = True
) -> Tuple[Type[Model], Collection]:
    """
    Return model class and Collection for a slug.

    Raises 404 if collection is unique (when required) or model not found.
    """
    collection = get_collection_by_slug(slug)
    if require_non_unique and collection.unique:
        raise Http404("Unique collections not allowed for entries.")

    model_class = get_model_for_slug(slug)
    if not model_class:
        raise Http404("No model found for slug.")

    return model_class, collection


def save_collection_instance(instance, data):
    """
    Speichert Daten in ein Collection-Model, inkl. ManyToMany-Felder.
    """
    # Zuerst alle normalen Felder setzen
    for key, value in data.items():
        field = instance._meta.get_field(key)
        if not field.many_to_many:
            setattr(instance, key, value)

    # Speichern, damit wir eine ID bekommen
    instance.save()

    # Jetzt ManyToMany-Felder setzen
    for key, value in data.items():
        field = instance._meta.get_field(key)
        if field.many_to_many:
            getattr(instance, key).set(value)

    return instance
