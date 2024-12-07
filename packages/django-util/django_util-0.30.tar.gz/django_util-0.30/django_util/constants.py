"""Constants module for Django field type definitions and collections.

This module defines type aliases and collections for Django field types,
particularly focusing on relationship and complex field types used across
the application.
"""

from typing import FrozenSet, Type, Union

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db.models import ManyToManyField, ManyToManyRel, ManyToOneRel

__all__ = [
    "related_fields",
    "complex_fields",
]

# Custom type aliases
RelatedFieldTypes = Union[
    Type[GenericRelation],
    Type[ManyToManyField],
    Type[ManyToManyRel],
    Type[ManyToOneRel],
]
"""Type alias for Django relationship field types.

Represents a union of various Django field types that handle model relationships,
including generic relations, many-to-many fields, and related field managers.
"""

# Field type collections
related_fields: FrozenSet[RelatedFieldTypes] = frozenset(
    {
        GenericRelation,
        ManyToManyField,
        ManyToManyRel,
        ManyToOneRel,
    }
)
"""FrozenSet of Django relationship field types.

An immutable set containing all Django field types that represent
relationships between models, including generic relations and
many-to-many relationships.
"""

complex_fields: FrozenSet[Type[ArrayField]] = frozenset({ArrayField})
"""FrozenSet of complex Django field types.

An immutable set containing Django field types that handle complex data structures,
currently only including PostgreSQL ArrayField.
"""
