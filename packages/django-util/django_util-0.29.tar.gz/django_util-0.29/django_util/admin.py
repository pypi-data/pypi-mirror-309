"""
Django admin utility module for field management and filtering.

This module provides utility functions and constants for configuring Django admin views,
particularly focused on field filtering and display configurations.

Attributes:
    related_field_set (Set[Type]): Set of Django field types that represent relations.
    complex_field_set (Set[Type]): Set of Django field types considered complex.
    list_display_user_admin (List[str]): Default display fields for User admin interface.
    list_display_exclude (List[Type]): Field types to exclude from admin list display.
    list_filter_base (List[str]): Base filter fields for standard admin views.
    list_filter_base_public_contribute (List[str]): Extended filter fields including verification status.
"""

from typing import Any, List, Set, Type

from django.db.models import ManyToManyField

from django_util.constants import complex_fields, related_fields

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
    """Gets field names from a Django model based on specified field types.

    Args:
        django_object (models.Model): Django model instance or class to inspect.
        field_types (List[Type[models.Field]]): List of Django field types to filter by.
        exclude (bool, optional): Whether to exclude or include the specified field types.
            Defaults to True.

    Returns:
        List[str]: List of field names that match the filtering criteria.

    Example:
        >>> fields = django_meta_get_fields(MyModel, [ManyToManyField], exclude=True)
        >>> print(fields)
        ['id', 'name', 'description']
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
    """Convenience wrapper for django_meta_get_fields that excludes specified field types.

    Args:
        django_object (Any): Django model instance or class to inspect.
        to_exclude (List[Type], optional): List of field types to exclude.
            Defaults to list_display_exclude.

    Returns:
        List[str]: List of field names excluding the specified field types.
    """
    return django_meta_get_fields(django_object, to_exclude, exclude=True)


def django_meta_get_fields_include(
    django_object: Any,
    to_include: List[Type] = [ManyToManyField],
) -> List[str]:
    """Convenience wrapper for django_meta_get_fields that includes only specified field types.

    Args:
        django_object (Any): Django model instance or class to inspect.
        to_include (List[Type], optional): List of field types to include.
            Defaults to [ManyToManyField].

    Returns:
        List[str]: List of field names matching the specified field types.
    """
    return django_meta_get_fields(django_object, to_include, exclude=False)
