# brickheadless/context_processors.py

"""
Context processors for injecting global settings into Django templates.
"""

from django.conf import settings


def vite_context(_request):
    """
    Add the VITE_DEV flag from Django settings to all template contexts.

    Args:
        _request: The current HttpRequest object (required by Django, unused).

    Returns:
        dict: A context dictionary with VITE_DEV set to True or False.
    """
    return {"VITE_DEV": getattr(settings, "VITE_DEV", False)}
