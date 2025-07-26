# brickheadless/templatetags/vite_tags.py

"""
Custom Django template tag to resolve Vite asset filenames using the manifest.
Use in templates via `{% vite_asset 'styles.css' %}` or `{% vite_asset 'app.bundle.js' %}`
"""

from django import template
from brickheadless.utils.vite import get_vite_asset

register = template.Library()


@register.simple_tag
def vite_asset(name: str) -> str:
    """
    Template tag to return the correct path to a Vite-built asset from the manifest.

    Example:
        {% vite_asset 'styles.css' %}
        {% vite_asset 'app.bundle.js' %}

    Args:
        name (str): Logical asset name (e.g. 'styles.css' or 'app.bundle.js')

    Returns:
        str: Public static path to the asset, or an empty string on failure.
    """
    try:
        return get_vite_asset(name)
    except (FileNotFoundError, KeyError):
        return ""
