from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    When User object is created, create Profile object using the custom Profile model
    specified in settings.PROFILE_MODEL or fallback to default Profile model
    """
    # Get the Profile model from settings or use default
    profile_model_path = getattr(settings, "PROFILE_MODEL", "django_util.Profile")
    Profile = apps.get_model(profile_model_path)

    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
