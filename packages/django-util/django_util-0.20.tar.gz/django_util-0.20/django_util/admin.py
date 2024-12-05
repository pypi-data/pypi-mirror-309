from typing import Any, List, Set, Type

from django.db.models import ManyToManyField

from django_util.constants import complex_fields, related_fields

"""
Django admin utility module for field management and filtering.

This module provides constants and utility functions for configuring Django admin views,
including field filtering, display configurations, and meta field operations.

Attributes:
    related_field_set: Set of related field types
    complex_field_set: Set of complex field types
    list_display_user_admin: Default user admin display fields
    list_display_exclude: Fields to exclude from admin display
    list_filter_base: Base filter fields for admin views
"""

# Convert field collections to sets for better performance
related_field_set: Set[Type] = set(related_fields)
complex_field_set: Set[Type] = set(complex_fields)

# Standard admin display fields
list_display_user_admin: List[str] = [
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "is_staff",
]

# Fields to exclude from list_display in admin
list_display_exclude: List[Type] = list(related_field_set | complex_field_set)

# Base filters for admin views
list_filter_base: List[str] = ["is_admin_verified"]
list_filter_base_public_contribute: List[str] = list_filter_base + ["is_verified"]


def django_meta_get_fields(
    django_object: "models.Model",
    field_types: List[Type["models.Field"]],
    exclude: bool = True,
) -> List[str]:
    """
    Get field names from a Django model based on field types.

    Args:
        django_object: Django model instance or class
        field_types: List of field types to filter by
        exclude: If True, exclude the specified field types; if False, include only these types

    Returns:
        List of field names matching the criteria
    """
    return [
        field.name
        for field in django_object._meta.get_fields()
        if exclude != isinstance(field, tuple(field_types))
    ]


# Maintain backward compatibility
def django_meta_get_fields_exclude(
    django_object: Any,
    to_exclude: List[Type] = list_display_exclude,
) -> List[str]:
    """Wrapper for django_meta_get_fields with exclude=True"""
    return django_meta_get_fields(django_object, to_exclude, exclude=True)


def django_meta_get_fields_include(
    django_object: Any,
    to_include: List[Type] = [ManyToManyField],
) -> List[str]:
    """Wrapper for django_meta_get_fields with exclude=False"""
    return django_meta_get_fields(django_object, to_include, exclude=False)
