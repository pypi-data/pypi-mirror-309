"""Django choice field definitions for various data types.

This module provides a collection of choice classes for use with Django models and forms.
Each class inherits from BaseChoices and provides standardized options for different
data types and business domains.

Categories:
    - Generic: Basic choice types like boolean, time frequency, etc.
    - Person: Demographic and personal information choices
    - Payment: Payment and transaction related choices

Example:
    from django_util.choices import TimeFrequencyChoices

    class Subscription(models.Model):
        frequency = models.CharField(
            max_length=50,
            choices=TimeFrequencyChoices.choices,
            default=TimeFrequencyChoices.DEFAULT
        )
"""

from datetime import timedelta
from typing import Dict, List, Optional, Set, Tuple, Union

from django.db import models
from django.utils.translation import gettext_lazy as _

# Choice categories for better organization
GENERIC_CHOICES = [
    "BaseChoices",
    "BooleanChoices",
    "FlatOrPercentChoices",
    "TimeFrequencyChoices",
    "TaskStatusChoices",
]

PERSON_CHOICES = [
    "PersonBloodChoices",
    "PersonEducationLevelChoices",
    "PersonEyeColorChoices",
    "PersonGenderChoices",
    "PersonRaceChoices",
]

PAYMENT_CHOICES = [
    "PaymentMethodTypeChoices",
    "TransactionGatewayChoices",
    "TransactionStateChoices",
    "TransactionTypeChoices",
    "TransactionEventTypeChoices",
]

__all__ = [
    *GENERIC_CHOICES,
    *PERSON_CHOICES,
    *PAYMENT_CHOICES,
]

TRUE_FALSE_CHOICES: List[Tuple[Union[bool, str], str]] = [
    ("", "---"),
    (True, "True"),
    (False, "False"),
]


class BaseChoices(models.TextChoices):
    """Base class providing common functionality for all choice classes.

    This class serves as the foundation for all choice classes in the module,
    providing standard utility methods and consistent behavior.

    Attributes:
        DEFAULT (str): Empty string choice with "---" label

    Methods:
        get_values(): Returns set of all valid values excluding DEFAULT
        get_labels(): Returns mapping of values to their display labels
        is_valid(value): Checks if a value is valid for this choice set
        get_label(value): Gets display label for a value
        exclude_default(): Returns choices without the DEFAULT option
    """

    DEFAULT = "", _("---")

    @classmethod
    def get_values(cls) -> Set[str]:
        """Return set of all valid values excluding DEFAULT.

        Returns:
            Set[str]: Set of all choice values except DEFAULT
        """
        return {choice[0] for choice in cls.choices if choice[0]}

    @classmethod
    def get_labels(cls) -> Dict[str, str]:
        """Return mapping of values to their display labels."""
        return {choice[0]: choice[1] for choice in cls.choices}

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is valid for this choice set."""
        return value in cls.get_values()

    @classmethod
    def get_label(cls, value: str) -> Optional[str]:
        """Get display label for a value."""
        return cls.get_labels().get(value)

    @classmethod
    def exclude_default(cls) -> List[Tuple[str, str]]:
        """Return choices without the DEFAULT option."""
        return [(k, v) for k, v in cls.choices if k != ""]


# Generic
class BooleanChoices(models.TextChoices):
    """Boolean choice options with an empty default.

    Provides a three-state boolean (True/False/None) for form fields.
    Includes utility method for converting string values to Python booleans.

    Attributes:
        DEFAULT (str): Empty string choice with "---" label
        YES (str): "TRUE" value with "Yes" label
        NO (str): "FALSE" value with "No" label

    Example:
        class Settings(models.Model):
            is_active = models.CharField(
                max_length=5,
                choices=BooleanChoices.choices,
                default=BooleanChoices.DEFAULT
            )
    """

    DEFAULT = "", _("---")
    YES = "TRUE", _("Yes")
    NO = "FALSE", _("No")

    @classmethod
    def to_python(cls, value: str) -> Optional[bool]:
        """Convert string value to Python boolean."""
        if value == cls.YES:
            return True
        if value == cls.NO:
            return False
        return None

    @classmethod
    def get_values(cls) -> Set[str]:
        """Return set of all valid values excluding DEFAULT."""
        return {choice[0] for choice in cls.choices if choice[0]}

    @classmethod
    def get_labels(cls) -> Dict[str, str]:
        """Return mapping of values to their display labels."""
        return {choice[0]: choice[1] for choice in cls.choices}

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is valid for this choice set."""
        return value in cls.get_values()

    @classmethod
    def get_label(cls, value: str) -> Optional[str]:
        """Get display label for a value."""
        return cls.get_labels().get(value)

    @classmethod
    def exclude_default(cls) -> List[Tuple[str, str]]:
        """Return choices without the DEFAULT option."""
        return [(k, v) for k, v in cls.choices if k != ""]


class FlatOrPercentChoices(BaseChoices):
    """Flat or percent choices for rate calculations.

    Attributes:
        FLAT (str): Flat rate option
        PERCENT (str): Percentage rate option
    """

    FLAT = "FLAT", _("Flat")
    PERCENT = "PERCENT", _("Percent")


class TimeFrequencyChoices(BaseChoices):
    """Time frequency options for recurring events.

    Provides standard time frequency options with utility methods for
    calculating durations and intervals.

    Attributes:
        HOURLY (str): Hourly frequency option
        DAILY (str): Daily frequency option
        WEEKLY (str): Weekly frequency option
        MONTHLY (str): Monthly frequency option
        QUARTERLY (str): Quarterly frequency option
        ANNUALLY (str): Annually frequency option

    Example:
        class Schedule(models.Model):
            frequency = models.CharField(
                max_length=20,
                choices=TimeFrequencyChoices.choices,
                default=TimeFrequencyChoices.DAILY
            )
    """

    HOURLY = "HOURLY", _("Hourly")
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    QUARTERLY = "QUARTERLY", _("Quarterly")
    ANNUALLY = "ANNUALLY", _("Annually")

    DURATION_MAPPING = {
        HOURLY: timedelta(hours=1),
        DAILY: timedelta(days=1),
        WEEKLY: timedelta(weeks=1),
        MONTHLY: timedelta(days=30),  # Approximate
        QUARTERLY: timedelta(days=91),  # Approximate
        ANNUALLY: timedelta(days=365),
    }

    @classmethod
    def get_timedelta(cls, frequency: str) -> Optional[timedelta]:
        """Get timedelta for a frequency value."""
        return cls.DURATION_MAPPING.get(frequency)

    @classmethod
    def get_seconds(cls, frequency: str) -> Optional[int]:
        """Get duration in seconds for a frequency."""
        delta = cls.get_timedelta(frequency)
        return int(delta.total_seconds()) if delta else None


class TaskStatusChoices(BaseChoices):
    """Task processing status options.

    Represents different states in a task's lifecycle from creation to completion.

    Attributes:
        PENDING (str): Task is waiting to be processed
        IN_PROGRESS (str): Task is currently being processed
        COMPLETED (str): Task has been successfully completed
        FAILED (str): Task has failed to complete
    """

    PENDING = "PENDING", _("Pending")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    COMPLETED = "COMPLETED", _("Completed")
    FAILED = "FAILED", _("Failed")

    # Add class methods for common validations
    @classmethod
    def is_terminal_state(cls, status):
        """Check if the status is in a terminal state (completed or failed)."""
        return status in {cls.COMPLETED, cls.FAILED}

    @classmethod
    def is_active_state(cls, status):
        """Check if the status is in an active state (pending or in progress)."""
        return status in {cls.PENDING, cls.IN_PROGRESS}


# Person
class PersonBloodChoices(BaseChoices):
    """Blood type classification options.

    Attributes:
        A (str): Blood type A
        B (str): Blood type B
        AB (str): Blood type AB
        O (str): Blood type O
        OTHERS (str): Other blood types
    """

    A = "A", _("A")
    B = "B", _("B")
    AB = "AB", _("AB")
    O = "O", _("O")
    OTHERS = "OTHERS", _("Others")


class PersonEducationLevelChoices(BaseChoices):
    """Academic achievement level classifications.

    Represents different levels of academic achievement from high school through doctoral degrees.

    References:
        https://study.com/different_degrees.html

    Attributes:
        HIGH_SCHOOL (str): High School diploma
        ASSOCIATE (str): Associate degree
        BACHELOR (str): Bachelor's degree
        MASTER (str): Master's degree
        DOCTORAL (str): Doctoral degree
        OTHERS (str): Other education levels
    """

    HIGH_SCHOOL = "HIGH_SCHOOL", _("High School")
    ASSOCIATE = "ASSOCIATE", _("Associate Degree")
    BACHELOR = "BACHELOR", _("Bachelor's Degree")
    MASTER = "MASTER", _("Master's Degree")
    DOCTORAL = "DOCTORAL", _("Doctoral Degree")
    OTHERS = "OTHERS", _("Others")

    # Add metadata as class attributes
    EDUCATION_YEARS = {
        HIGH_SCHOOL: 12,
        ASSOCIATE: 14,
        BACHELOR: 16,
        MASTER: 18,
        DOCTORAL: 20,
    }

    @classmethod
    def get_education_years(cls, level: str) -> int:
        """Return typical years of education for given level."""
        return cls.EDUCATION_YEARS.get(level, 0)


class PersonEyeColorChoices(BaseChoices):
    """Eye color classification options.

    References:
        https://en.wikipedia.org/wiki/Eye_color#Eye_color_chart_(Martin_scale)

    Attributes:
        AMBER (str): Amber colored eyes
        BLUE (str): Blue colored eyes
        BROWN (str): Brown colored eyes
        GREEN (str): Green colored eyes
        GREY (str): Grey colored eyes
        HAZEL (str): Hazel colored eyes
        RED (str): Red colored eyes
        OTHERS (str): Other eye colors
    """

    AMBER = "AMBER", _("Amber")
    BLUE = "BLUE", _("Blue")
    BROWN = "BROWN", _("Brown")
    GREEN = "GREEN", _("Green")
    GREY = "GREY", _("Grey")
    HAZEL = "HAZEL", _("Hazel")
    RED = "RED", _("Red")
    OTHERS = "OTHERS", _("Others")


class PersonGenderChoices(BaseChoices):
    """Gender classification options.

    Attributes:
        FEMALE (str): Female gender
        MALE (str): Male gender
        OTHERS (str): Other gender identifications
    """

    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    OTHERS = "OTHERS", _("Others")


class PersonRaceChoices(BaseChoices):
    """Racial and ethnic classification options.

    References:
        https://grants.nih.gov/grants/guide/notice-files/not-od-15-089.html

    Attributes:
        ASIAN (str): Asian racial identification
        BLACK (str): Black or African American racial identification
        HISPANIC (str): Hispanic or Latino ethnic identification
        INDIAN (str): American Indian or Alaska Native racial identification
        ISLANDER (str): Native Hawaiian or Other Pacific Islander racial identification
        WHITE (str): White racial identification
        OTHERS (str): Other racial or ethnic identifications
    """

    ASIAN = "ASIAN", _("Asian")
    BLACK = "BLACK", _("Black Or African American")
    HISPANIC = "HISPANIC", _("Hispanic Or Latino")
    INDIAN = "INDIAN", _("American Indian Or Alaska Native")
    ISLANDER = "ISLANDER", _("Native Hawaiian Or Other Pacific Islander")
    WHITE = "WHITE", _("White")
    OTHERS = "OTHERS", _("Others")


# Payment / Transaction
class PaymentMethodTypeChoices(BaseChoices):
    """Available payment method options.

    Attributes:
        CREDIT_CARD (str): Credit card payment method
        DEBIT_CARD (str): Debit card payment method
        ELECTRONIC_BANK_TRANSFER (str): Bank transfer payment method
        PAYPAL (str): PayPal payment method
        APPLE_PAY (str): Apple Pay payment method
        GOOGLE_PAY (str): Google Pay payment method
    """

    CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
    DEBIT_CARD = "DEBIT_CARD", _("Debit Card")
    ELECTRONIC_BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")
    PAYPAL = "PAYPAL", _("PayPal")
    APPLE_PAY = "APPLE_PAY", _("Apple Pay")
    GOOGLE_PAY = "GOOGLE_PAY", _("Google Pay")

    REQUIRES_CVV = {CREDIT_CARD, DEBIT_CARD}
    REQUIRES_3DS = {CREDIT_CARD, DEBIT_CARD}

    @classmethod
    def requires_cvv(cls, method: str) -> bool:
        """Check if payment method requires CVV."""
        return method in cls.REQUIRES_CVV

    @classmethod
    def requires_3ds(cls, method: str) -> bool:
        """Check if payment method requires 3D Secure."""
        return method in cls.REQUIRES_3DS

    @classmethod
    def card_methods(cls) -> set:
        """Return all card-based payment methods."""
        return {cls.CREDIT_CARD, cls.DEBIT_CARD}

    @classmethod
    def digital_wallet_methods(cls) -> set:
        """Return all digital wallet payment methods."""
        return {cls.PAYPAL, cls.APPLE_PAY, cls.GOOGLE_PAY}


class TransactionGatewayChoices(BaseChoices):
    """Supported payment processing gateways.

    Attributes:
        ADYEN (str): Adyen payment gateway
        ALIPAY (str): Alipay payment gateway
        AMAZON (str): Amazon payment gateway
        AUTHORIZE (str): Authorize.net payment gateway
        BRAINTREE (str): Braintree payment gateway
        CYBERSOURCE (str): Cybersource payment gateway
        INGENICO (str): Ingenico payment gateway
        PAYPAL (str): PayPal payment gateway
        SQUARE (str): Square payment gateway
        STRIPE (str): Stripe payment gateway
        WEPAY (str): WePay payment gateway
        WORLDPAY (str): Worldpay payment gateway
    """

    ADYEN = "ADYEN", _("Adyen")
    ALIPAY = "ALIPAY", _("Alipay")
    AMAZON = "AMAZON", _("Amazon")
    AUTHORIZE = "AUTHORIZE", _("Authorize")
    BRAINTREE = "BRAINTREE", _("Braintree")
    CYBERSOURCE = "CYBERSOURCE", _("Cybersource")
    INGENICO = "INGENICO", _("Ingenico")
    PAYPAL = "PAYPAL", _("Paypal")
    SQUARE = "SQUARE", _("Square")
    STRIPE = "STRIPE", _("Stripe")
    WEPAY = "WEPAY", _("Wepay")
    WORLDPAY = "WORLDPAY", _("Worldpay")


class TransactionStateChoices(BaseChoices):
    """Transaction processing state options.

    References:
        https://stripe.com/docs/payments/intents#intent-statuses

    Attributes:
        REQUIRES_PAYMENT_METHOD (str): Payment method needs to be provided
        REQUIRES_CONFIRMATION (str): Transaction requires confirmation
        REQUIRES_ACTION (str): Additional action required
        PROCESSING (str): Transaction is being processed
        CANCEL (str): Transaction has been cancelled
        SUCCESS (str): Transaction completed successfully
    """

    REQUIRES_PAYMENT_METHOD = "REQUIRES_PAYMENT_METHOD", _("Requires Payment Method")
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION", _("Requires Confirmation")
    REQUIRES_ACTION = "REQUIRES_ACTION", _("Requires Action")
    PROCESSING = "PROCESSING", _("Processing")
    CANCEL = "CANCEL", _("Cancel")
    SUCCESS = "SUCCESS", _("Success")

    @classmethod
    def can_transition_to(cls, current_state: str, new_state: str) -> bool:
        """Validate if a state transition is allowed."""
        VALID_TRANSITIONS = {
            cls.DEFAULT: {cls.REQUIRES_PAYMENT_METHOD},
            cls.REQUIRES_PAYMENT_METHOD: {cls.REQUIRES_CONFIRMATION, cls.CANCEL},
            cls.REQUIRES_CONFIRMATION: {
                cls.REQUIRES_ACTION,
                cls.PROCESSING,
                cls.CANCEL,
            },
            cls.REQUIRES_ACTION: {cls.PROCESSING, cls.CANCEL},
            cls.PROCESSING: {cls.SUCCESS, cls.CANCEL},
            cls.SUCCESS: set(),  # Terminal state
            cls.CANCEL: set(),  # Terminal state
        }
        return new_state in VALID_TRANSITIONS.get(current_state, set())


class TransactionTypeChoices(BaseChoices):
    """Transaction classification options.

    Attributes:
        PAYMENT (str): Standard payment transaction
        REFUND (str): Refund transaction
        ADJUSTMENT (str): Adjustment transaction
        COUPON (str): Coupon application transaction
        PRORATION (str): Proration transaction
    """

    PAYMENT = "PAYMENT", _("Payment")
    REFUND = "REFUND", _("Refund")
    ADJUSTMENT = "ADJUSTMENT", _("Adjustment")
    COUPON = "COUPON", _("Coupon")
    PRORATION = "PRORATION", _("Proration")

    AFFECTS_BALANCE = {PAYMENT, REFUND, ADJUSTMENT}
    REQUIRES_PROCESSING = {PAYMENT, REFUND}

    @classmethod
    def affects_balance(cls, trans_type: str) -> bool:
        """Check if transaction type affects account balance."""
        return trans_type in cls.AFFECTS_BALANCE

    @classmethod
    def requires_processing(cls, trans_type: str) -> bool:
        """Check if transaction type requires payment processing."""
        return trans_type in cls.REQUIRES_PROCESSING


class TransactionEventTypeChoices(BaseChoices):
    """Transaction lifecycle event types.

    Attributes:
        CREATED (str): Transaction has been created
        AUTHORIZED (str): Transaction has been authorized
        CAPTURED (str): Transaction has been captured
        REFUNDED (str): Transaction has been refunded
        FAILED (str): Transaction has failed
    """

    CREATED = "CREATED", _("Created")
    AUTHORIZED = "AUTHORIZED", _("Authorized")
    CAPTURED = "CAPTURED", _("Captured")
    REFUNDED = "REFUNDED", _("Refunded")
    FAILED = "FAILED", _("Failed")
