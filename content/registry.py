"""Registry für dynamisch generierte Collection-Modelle."""

_registered_models = {}


def register_collection_model(slug, model_class):
    """
    Registriert ein dynamisches Modell unter einem eindeutigen Slug.
    Fügt die nötigen Metadaten hinzu, damit Django das Modell erkennt.
    """
    # pylint: disable=protected-access
    model_class._meta.app_label = "content"
    # pylint: enable=protected-access
    model_class.__module__ = "content.models"

    _registered_models[slug] = model_class
    return model_class


def get_registered_models():
    """Gibt alle registrierten dynamischen Modelle zurück."""
    return _registered_models
