"""
Renders a field by matching its type to a template.
"""

from django.template.loader import render_to_string


def render_field(field, name=None, value=None):
    """
    Renders a field using its admin template.

    Args:
        field (BaseField): Field definition from schema (cms.py)
        name (str, optional): Input name used in the form (defaults to field.name)
        value (Any, optional): Pre-filled value (defaults to "")

    Returns:
        str: Rendered HTML for the admin UI
    """
    name = name or field.name  # fallback for templates that expect "name"
    value = value or ""

    return render_to_string(
        f"bricks_admin/fields/{field.type}.html",
        {
            "field": field,
            "name": name,
            "value": value,
        },
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
