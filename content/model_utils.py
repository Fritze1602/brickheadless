from content import generated_models


def get_model_for_slug(slug: str):
    """
    Holt die passende Modelklasse für eine Collection, z. B. "projects" → ProjectsEntry
    """
    class_name = "".join(word.capitalize() for word in slug.split("_")) + "Entry"
    return getattr(generated_models, class_name, None)
