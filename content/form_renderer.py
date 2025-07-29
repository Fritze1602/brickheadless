"""
Renders a field by matching its type to a template.
"""

from django.template.loader import render_to_string
from content.model_utils import get_model_for_slug


def render_field(field, name=None, value=None, options=None):
    """
    Renders a field using its admin template.

    Args:
        field (BaseField): Field definition from schema (cms.py)
        name (str, optional): Input name used in the form (defaults to field.name)
        value (Any, optional): Pre-filled value (defaults to "")
        options (QuerySet | list, optional): Used for relation fields

    Returns:
        str: Rendered HTML for the admin UI
    """
    name = name or field.name
    value = value or ""

    context = {
        "field": field,
        "name": name,
        "value": value,
    }

    if field.type == "relation" and options is not None:
        context["options"] = options

    return render_to_string(
        f"bricks_admin/fields/{field.type}.html",
        context,
    )


def extract_data(fields, post_data, files_data):
    """
    Extracts form data from a POST request based on BrickField definitions.

    Supported field types: text, url, relation, repeater.
    Repeater fields are parsed using the naming scheme like 'ctas[0][text]'.

    Returns:
        dict: Structured values matching the page or collection schema.
    """
    result = {}

    for field in fields:
        if field.type in ("text", "url"):
            result[field.name] = post_data.get(field.name)

        elif field.type == "relation":
            # Multi-select checkbox values
            result[field.name] = post_data.getlist(field.name)

        elif field.type == "repeater":
            prefix = field.name + "["
            items = {}

            for key, value in post_data.items():
                if key.startswith(prefix):
                    parts = key[len(field.name) :].strip("[]").split("][")
                    if len(parts) != 2:
                        continue
                    try:
                        index = int(parts[0])
                    except ValueError:
                        continue
                    subfield_name = parts[1]
                    items.setdefault(index, {})
                    items[index][subfield_name] = value

            result[field.name] = [items[i] for i in sorted(items.keys())]

        else:
            raise NotImplementedError(
                f"extract_data: Feldtyp '{field.type}' wird noch nicht unterstützt."
            )

    return result


def render_page_fields(page_obj, data):
    """
    Renders fields for a Page object.
    """
    return [
        {
            "label": field.label,
            "html": render_field(field, field.name, data.get(field.name)),
        }
        for field in page_obj.fields
    ]


def get_initial_value(field, instance, pk=None):
    """
    Gibt den initialen Wert für ein Feld zurück.
    Bei Relation-Feldern mit ManyToMany wird eine Liste der IDs zurückgegeben.
    """
    if getattr(field, "type", None) == "relation" and getattr(field, "many", False):
        if pk is not None:
            rel = getattr(instance, field.name, None)
            if rel is not None and hasattr(rel, "values_list"):
                ids = list(rel.values_list("id", flat=True))
                return [str(pk) for pk in ids]
        return []
    return getattr(instance, field.name, None) or ""


def get_relation_options(field):
    """
    Gibt alle möglichen Optionen für ein Relation-Feld zurück.
    """
    if getattr(field, "type", None) == "relation":
        related_model = get_model_for_slug(field.to)
        return related_model.objects.all()
    return None


def render_collection_fields(collection, instance):
    """
    Rendert alle Felder einer Collection mit den gegebenen Daten vorbefüllt.
    """
    rendered = []
    for field in collection.fields:
        value = get_initial_value(field, instance)
        options = get_relation_options(field)
        html = render_field(field, field.name, value, options=options)
        rendered.append({"label": field.label, "html": html})
    return rendered
