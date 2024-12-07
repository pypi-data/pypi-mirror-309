from django.utils.functional import lazy
from django.utils.safestring import mark_safe


def is_object_creator(object, profile):
    """Check if the given profile is the creator of the object.

    Args:
        object: The object to check ownership of.
        profile: The profile to verify as the creator.

    Returns:
        bool: True if the profile is the creator of the object, False otherwise.
    """
    return object.profile == profile


mark_safe_lazy = lazy(mark_safe, str)
"""Deprecated: A lazy wrapper for mark_safe function.

This function is deprecated and obsolete as of Django 4.1. It was previously used
to create lazy versions of marked-safe strings, typically for form help text with HTML.

See:
    https://docs.djangoproject.com/en/4.1/releases/4.1/#utilities
"""
