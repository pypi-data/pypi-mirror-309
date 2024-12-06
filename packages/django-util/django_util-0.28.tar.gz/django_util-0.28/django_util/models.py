import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from django_util.choices import (
    FlatOrPercentChoices,
    PaymentMethodTypeChoices,
    PersonBloodChoices,
    PersonEyeColorChoices,
    PersonGenderChoices,
    PersonRaceChoices,
    TimeFrequencyChoices,
    TransactionEventTypeChoices,
    TransactionStateChoices,
    TransactionTypeChoices,
)
from django_util.constants import complex_fields, related_fields
from django_util.fields import UpperTextField


# abstract
class Profile(models.Model):
    """Abstract profile model that extends Django User model.

    Provides one-to-one relationship with Django's built-in User model.

    Attributes:
        user (User): One-to-one relationship to Django User model.

    References:
        https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Base(models.Model):
    """Abstract base model with metadata and user tracking.

    Provides created/updated timestamps, user tracking, notes and verification.

    Attributes:
        created_at (datetime): Timestamp of creation
        updated_at (datetime): Timestamp of last update
        created_by (User): User who created the record
        updated_by (User): User who last updated the record
        note (str): Upper case text field for notes
        is_admin_verified (bool): Whether verified by admin

    References:
        - https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes
        - https://dataedo.com/kb/data-glossary/what-is-metadata
        - https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/#models-and-request-user
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_by = models.ForeignKey(
        getattr(settings, "PROFILE_MODEL", "auth.User"),
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        getattr(settings, "PROFILE_MODEL", "auth.User"),
        editable=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
    )
    note = UpperTextField(
        blank=True,
        default="",
    )
    is_admin_verified = models.BooleanField(
        default=False,
        editable=False,
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_base_meta_field_list() -> list:
        return sorted(
            [
                "created_at",
                "updated_at",
            ]
        )

    @staticmethod
    def get_extra_meta_field_list() -> list:
        return sorted(
            [
                "created_by",
                "updated_by",
                "note",
                "is_admin_verified",
            ]
        )

    @classmethod
    def get_field_list(cls):
        return sorted([field.name for field in cls._meta.get_fields()])

    @classmethod
    def get_field_list_without_extra_meta(cls):
        return sorted(
            list(set(cls.get_field_list()) - set(cls.get_extra_meta_field_list()))
        )

    @classmethod
    def get_field_list_without_meta(cls):
        return sorted(
            list(
                set(cls.get_field_list())
                - set(cls.get_base_meta_field_list())
                - set(cls.get_extra_meta_field_list())
            )
        )

    @classmethod
    def get_related_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, related_fields):
                field_list.append(field.name)
        return sorted(field_list)

    @classmethod
    def get_complex_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, complex_fields):
                field_list.append(field.name)
        return sorted(field_list)


class BasePublicContribute(Base):
    """Enhanced base model for publicly editable data.

    Extends Base model with verification and visibility controls.

    Attributes:
        is_verified (bool): Whether the entry has been verified
        is_hidden (bool): Whether the entry should be hidden from public view
    """

    is_verified = models.BooleanField(
        default=False,
    )
    is_hidden = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_staff_only_field_list():
        return sorted(
            [
                "is_hidden",
                "is_verified",
            ]
        )


class EmailHttpRequest(models.Model):
    """Abstract model for storing email and HTTP request data.

    Attributes:
        email (str): Email address with database index
        campaign (str): Upper case campaign identifier
        http_referrer (str): HTTP referrer URL
        http_user_agent (str): User agent string
        remote_addr (str): IP address of requester
        remote_host (str): Hostname of requester
    """

    email = models.EmailField(
        db_index=True,
    )
    campaign = UpperTextField(
        blank=True,
        default="",
    )
    http_referrer = UpperTextField(
        blank=True,
        default="",
    )
    http_user_agent = UpperTextField(
        blank=True,
        default="",
    )
    remote_addr = models.GenericIPAddressField(
        blank=True,
        null=True,
    )
    remote_host = UpperTextField(
        blank=True,
        default="",
    )

    class Meta:
        abstract = True


class Person(models.Model):
    """Abstract model for storing person information.

    Stores comprehensive personal information including names, physical characteristics,
    and biographical data.

    Attributes:
        uuid (UUID): Unique identifier
        english_first_name (str): First name in English
        english_middle_name (str): Middle name in English
        english_last_name (str): Last name in English
        native_first_name (str): First name in native language
        native_middle_name (str): Middle name in native language
        native_last_name (str): Last name in native language
        alias (list): List of alternative names
        description (str): General description
        birth_date (datetime): Date of birth
        death_date (datetime): Date of death
        blood_type (str): Blood type
        eye_color (str): Eye color
        gender (str): Gender identity
        race (str): Racial identity
        height (int): Height in units

    References:
        https://schema.org/Person
    """

    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    english_first_name = UpperTextField(
        blank=True,
        default="",
    )
    english_middle_name = UpperTextField(
        blank=True,
        default="",
    )
    english_last_name = UpperTextField(
        blank=True,
        default="",
    )
    native_first_name = UpperTextField(
        blank=True,
        default="",
    )
    native_middle_name = UpperTextField(
        blank=True,
        default="",
    )
    native_last_name = UpperTextField(
        blank=True,
        default="",
    )
    alias = ArrayField(
        UpperTextField(),
        blank=True,
        null=True,
    )
    description = UpperTextField(
        blank=True,
        default="",
    )

    # biology
    birth_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    death_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    blood_type = UpperTextField(
        blank=True,
        choices=PersonBloodChoices.choices,
        default=PersonBloodChoices.DEFAULT,
    )
    eye_color = UpperTextField(
        blank=True,
        choices=PersonEyeColorChoices.choices,
        default=PersonEyeColorChoices.DEFAULT,
    )
    gender = UpperTextField(
        blank=True,
        choices=PersonGenderChoices.choices,
        default=PersonGenderChoices.DEFAULT,
    )
    race = UpperTextField(
        blank=True,
        choices=PersonRaceChoices.choices,
        default=PersonRaceChoices.DEFAULT,
    )
    height = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        abstract = True


class FullCalendarEventParseV6(models.Model):
    """Abstract model for FullCalendar v6 event data.

    Stores all fields needed for FullCalendar event parsing and display.

    Attributes:
        group_id (str): Event group identifier
        all_day (bool): Whether event is all-day
        start (datetime): Event start time
        end (datetime): Event end time
        days_of_week (list): Days when event repeats
        start_time (time): Start time for recurring events
        end_time (time): End time for recurring events
        start_recur (datetime): Recurrence start date
        end_recur (datetime): Recurrence end date
        title (str): Event title
        url (str): Associated URL
        interactive (bool): Whether event is interactive
        class_name (list): CSS classes to apply
        editable (bool): Whether event is editable
        start_editable (bool): Whether start time is editable
        duration_editable (bool): Whether duration is editable
        resource_editable (bool): Whether resource is editable
        resource_id (str): Associated resource ID
        resource_ids (list): Multiple associated resource IDs
        display (str): Display mode
        overlap (bool): Whether event can overlap
        constraint (bool): Event constraints
        color (bool): Event color

    References:
        https://fullcalendar.io/docs/v6/event-parsing
    """

    group_id = models.TextField(
        blank=True,
        default="",
    )
    all_day = models.BooleanField(
        blank=True,
        null=True,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
    )
    end = models.DateTimeField(
        blank=True,
        null=True,
    )
    days_of_week = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    start_time = models.TimeField(
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        blank=True,
        null=True,
    )
    start_recur = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_recur = models.DateTimeField(
        blank=True,
        null=True,
    )
    title = models.TextField(
        blank=True,
        default="",
    )
    url = models.URLField(
        blank=True,
        default="",
    )
    interactive = models.BooleanField(
        blank=True,
        null=True,
    )
    class_name = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    editable = models.BooleanField(
        blank=True,
        null=True,
    )
    start_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    duration_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    resource_editable = models.BooleanField(
        blank=True,
        null=True,
    )
    resource_id = models.TextField(
        blank=True,
        default="",
    )
    resource_ids = ArrayField(
        models.TextField(),
        blank=True,
        null=True,
    )
    display = models.TextField(
        blank=True,
        default="",
    )
    overlap = models.BooleanField(
        blank=True,
        null=True,
    )
    constraint = models.BooleanField(
        blank=True,
        null=True,
    )
    color = models.BooleanField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class WiseWebhook(models.Model):
    """Abstract model for Wise webhook data.

    Stores webhook payload data from Wise payment service.

    Attributes:
        data (dict): Webhook payload data
        subscription_id (str): Subscription identifier
        event_type (str): Type of webhook event
        schema_version (str): Version of webhook schema
        sent_at (datetime): When webhook was sent

    References:
        https://docs.wise.com/api-docs/api-reference/webhook
    """

    data = models.JSONField(
        blank=True,
        default=dict,
    )
    subscription_id = models.TextField(
        blank=True,
        default="",
    )
    event_type = models.TextField(
        blank=True,
        default="",
    )
    schema_version = models.TextField(
        blank=True,
        default="",
    )
    sent_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Transaction(models.Model):
    """Abstract model for monetary transactions.

    Records monetary exchanges related to subscriptions including payments and refunds.

    Attributes:
        amount (Decimal): Total monetary value including taxes, fees etc
        currency (str): 3-letter currency code
        choice_type (str): Type of transaction
        data (dict): Additional transaction data
        state (str): Current transaction state
        transaction_date (datetime): When transaction occurred

    Notes:
        Transaction Amount includes total value with all fees and adjustments.
        Transaction Price refers to base price before additional charges.
    """

    amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    currency = UpperTextField(
        max_length=3,
        blank=True,
    )
    choice_type = UpperTextField(
        blank=True,
        choices=TransactionTypeChoices.choices,
        default=TransactionTypeChoices.DEFAULT,
    )
    data = models.JSONField(
        blank=True,
        default=dict,
    )
    state = UpperTextField(
        blank=True,
        choices=TransactionStateChoices.choices,
        default=TransactionStateChoices.DEFAULT,
    )
    transaction_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    # Relation
    # payment_method = models.ForeignKey
    # subscription = models.ForeignKey

    class Meta:
        abstract = True


class TransactionEvent(models.Model):
    """Abstract model for transaction lifecycle events.

    Records specific actions or state changes within a transaction's lifecycle.

    Attributes:
        choice_type (str): Type of event
        description (str): Event description
        data (dict): Additional event data
    """

    choice_type = UpperTextField(
        blank=True,
        choices=TransactionEventTypeChoices.choices,
        default=TransactionEventTypeChoices.DEFAULT,
    )
    description = UpperTextField(
        blank=True,
        default="",
    )
    data = models.JSONField(
        blank=True,
        default=dict,
    )

    # Relation
    # transaction = models.ForeignKey

    class Meta:
        abstract = True


class PaymentMethod(models.Model):
    """Abstract model for payment methods.

    Attributes:
        choice_type (str): Type of payment method
        billing_address (str): Associated billing address
    """

    choice_type = UpperTextField(
        blank=True,
        choices=PaymentMethodTypeChoices.choices,
        default=PaymentMethodTypeChoices.DEFAULT,
    )
    billing_address = models.TextField(
        blank=True,
        default="",
    )

    # Relation
    # profile = models.ForeignKey

    class Meta:
        abstract = True


class CardPayment(PaymentMethod):
    """Abstract model for card payment methods.

    Extends PaymentMethod with card-specific fields.

    Attributes:
        card_number (str): Card number
        card_expiry (datetime): Card expiration date
        card_cvv (str): Card security code
    """

    card_number = models.TextField(
        blank=True,
        default="",
    )
    card_expiry = models.DateTimeField(
        blank=True,
        null=True,
    )
    card_cvv = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        abstract = True


class Coupon(models.Model):
    """Abstract model for discount coupons.

    Attributes:
        code (str): Coupon code
        discount_type (str): Type of discount (flat or percentage)
        discount_value (Decimal): Amount of discount
        expiry_date (datetime): When coupon expires
        usage_limit (int): Maximum number of uses
    """

    code = models.TextField(
        blank=True,
        default="",
    )
    discount_type = UpperTextField(
        blank=True,
        choices=FlatOrPercentChoices.choices,
        default=FlatOrPercentChoices.DEFAULT,
    )
    discount_value = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    usage_limit = models.IntegerField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Plan(models.Model):
    """Abstract model for subscription plans.

    Defines features, pricing, and billing cycle for subscriptions.

    Attributes:
        name (str): Plan name
        description (str): Plan description
        price (Decimal): Plan price
        currency (str): 3-letter currency code
        billing_cycle (str): Frequency of billing
        feature (list): List of plan features
    """

    name = UpperTextField(
        blank=True,
        default="",
    )
    description = UpperTextField(
        blank=True,
        default="",
    )
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    currency = UpperTextField(
        max_length=3,
        blank=True,
    )
    billing_cycle = UpperTextField(
        blank=True,
        choices=TimeFrequencyChoices.choices,
        default=TimeFrequencyChoices.DEFAULT,
    )
    feature = ArrayField(
        UpperTextField(),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class PlanPlus(Plan):
    """Enhanced subscription plan model.

    Extends Plan with additional features.

    Attributes:
        trial_period (int): Length of trial period
        discount_eligible (bool): Whether plan can be discounted
    """

    trial_period = models.IntegerField(
        blank=True,
        null=True,
    )
    discount_eligible = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class Subscription(models.Model):
    """Abstract model for active subscriptions.

    Tracks customer subscription status and billing details.

    Attributes:
        start_date (datetime): When subscription begins
        end_date (datetime): When subscription ends
        next_billing_date (datetime): Next payment due date
        prorated_amount (Decimal): Prorated charge amount
        is_active (bool): Whether subscription is currently active
    """

    start_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    next_billing_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    prorated_amount = models.DecimalField(
        blank=True,
        null=True,
        max_digits=19,
        decimal_places=4,
    )
    is_active = models.BooleanField(
        default=False,
    )

    # Relation
    # coupon = models.ForeignKey
    # plan = models.ForeignKey
    # profile = models.ForeignKey

    class Meta:
        abstract = True
