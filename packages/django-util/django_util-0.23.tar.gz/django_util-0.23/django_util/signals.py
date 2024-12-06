from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creates or updates a user profile when a User object is saved.

    This signal handler automatically creates a Profile object for newly created
    User instances, or updates existing Profile objects for existing users.
    The Profile model can be customized via settings.PROFILE_MODEL.

    Args:
        sender: The model class that sent the signal (User).
        instance: The actual instance of the User model being saved.
        created (bool): True if a new record was created, False for updates.
        **kwargs: Additional keyword arguments passed by the signal.

    Returns:
        None

    Note:
        The Profile model is determined by settings.PROFILE_MODEL, defaulting to
        'django_util.Profile' if not specified.
    """
    # Get the Profile model from settings or use default
    profile_model_path = getattr(settings, "PROFILE_MODEL", "django_util.Profile")
    Profile = apps.get_model(profile_model_path)

    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
