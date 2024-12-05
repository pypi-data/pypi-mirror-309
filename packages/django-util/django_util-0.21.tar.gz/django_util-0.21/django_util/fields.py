from typing import Any
from urllib.parse import urlparse

from django.db import models


# class
class UpperTextField(models.TextField):
    """
    A TextField that is stripped and uppercase

    Examples
    --------
    >>> field = UpperTextField()
    >>> field.get_prep_value(" hello world ")
    'HELLO WORLD'
    >>> field.get_prep_value(None)
    None
    """

    def get_prep_value(self, value: Any) -> str | None:
        try:
            return str(value).strip().upper()
        except (TypeError, AttributeError):
            return None


class NoParamURLField(models.URLField):
    """
    A URLField that stores URLs without query parameters or fragments.
    Only preserves the network location (domain) and path components.

    Examples
    --------
    >>> field = NoParamURLField()
    >>> field.get_prep_value('https://example.com/path?query=1#fragment')
    'example.com/path'
    """

    def get_prep_value(self, value: Any) -> str | None:
        try:
            parsed = urlparse(value)
            return parsed.netloc + parsed.path
        except Exception:
            return None

    def validate(self, value: Any, model_instance) -> None:
        if value and not (urlparse(value).netloc and urlparse(value).path):
            from django.core.exceptions import ValidationError

            raise ValidationError("URL must contain both domain and path")
        super().validate(value, model_instance)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(max_length={self.max_length})"
