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

# Field type collections
related_fields: FrozenSet[RelatedFieldTypes] = frozenset(
    {
        GenericRelation,
        ManyToManyField,
        ManyToManyRel,
        ManyToOneRel,
    }
)

complex_fields: FrozenSet[Type[ArrayField]] = frozenset({ArrayField})
