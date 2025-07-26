# content/form_renderer.py

from django.template.loader import render_to_string


def render_field(field, name=None, value=None):
    """
    Rendert ein Feld (text, url, repeater) via Template.
    """
    name = name or field.name  # ⬅ fallback für Templates, die "name" nicht setzen
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
    Extrahiert Formulardaten gemäß Felddefinition.

    Unterstützt: text, url, repeater.
    Repeater-Felder werden anhand des Namenschemas wie 'ctas[0][text]' zu Listen geparst.

    Rückgabe: Dictionary mit strukturierten Werten passend zum Pages-Schema.
    """
    result = {}

    for field in fields:
        if field.type in ("text", "url"):
            result[field.name] = post_data.get(field.name)

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
