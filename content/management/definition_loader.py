import importlib
import inspect
from content.schema import Page, Collection


def load_definitions_from_module(module_path="content.pages"):
    """
    Lädt alle Page- und Collection-Definitionen aus einem Modul.
    Gibt zwei Listen zurück: (pages, collections)
    """
    module = importlib.import_module(module_path)

    pages = []
    collections = []

    for name, obj in inspect.getmembers(module):
        if isinstance(obj, Page):
            pages.append(obj)
        elif isinstance(obj, Collection):
            collections.append(obj)

    return pages, collections
