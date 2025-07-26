from django import template

register = template.Library()


@register.filter
def get_item(dict_obj, key):
    """
    Gibt dict[key] oder "" zurück, falls key fehlt.
    """
    return dict_obj.get(key, "")


@register.simple_tag
def field_name(parent, index, key):
    """
    Baut einen verschachtelten Feldnamen für Repeater-Felder.

    Beispiel:
        field_name("ctas", 0, "text") → 'ctas[0][text]'
    """
    return f"{parent}[{index}][{key}]"
