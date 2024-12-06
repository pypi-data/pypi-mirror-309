from django.core.validators import RegexValidator

is_numeric = RegexValidator(r"^[0-9]*$", "Only numbers, leading zeros are ok.")
"""RegexValidator: Validates that a string contains only numeric characters.

This validator ensures that the input string consists solely of digits (0-9).
Leading zeros are permitted in the input.

Examples:
    Valid inputs: "123", "001", "0", ""
    Invalid inputs: "12a", "-1", "1.0", "1,000"

Attributes:
    regex (str): The regular expression pattern "^[0-9]*$"
    message (str): The error message displayed when validation fails
"""
