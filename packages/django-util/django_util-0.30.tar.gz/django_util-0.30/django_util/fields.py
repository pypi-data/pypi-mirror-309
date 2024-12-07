from typing import Any
from urllib.parse import urlparse

from django.db import models


# class
class UpperTextField(models.TextField):
    """A TextField that converts input to uppercase and strips whitespace.

    This field extends Django's TextField to automatically convert stored values
    to uppercase and remove leading/trailing whitespace.

    Args:
        *args: Variable length argument list passed to TextField.
        **kwargs: Arbitrary keyword arguments passed to TextField.

    Returns:
        str: The processed string in uppercase with stripped whitespace.
        None: If the input cannot be converted to a string.

    Examples:
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
    """A URLField that stores URLs without query parameters or fragments.

    This field extends Django's URLField to store only the domain and path components
    of URLs, stripping away query parameters and fragments.

    Args:
        *args: Variable length argument list passed to URLField.
        **kwargs: Arbitrary keyword arguments passed to URLField.

    Returns:
        str: The processed URL containing only domain and path.
        None: If the input cannot be parsed as a valid URL.

    Raises:
        ValidationError: If the URL doesn't contain both domain and path components.

    Examples:
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
