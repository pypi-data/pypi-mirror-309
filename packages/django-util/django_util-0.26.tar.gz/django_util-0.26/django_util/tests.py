from django.contrib.auth.models import User
from django.test import TestCase

from django_util.models import Profile


# Create your tests here.
def user_example1(**kwargs):
    """Creates and returns a test user with default credentials.

    Args:
        **kwargs: Additional fields to be passed to User.objects.create()

    Returns:
        User: A newly created User instance with default username and password
    """
    user = User.objects.create(username="your_username", password="your_password")
    user.save()
    return user


class UserModelTests(TestCase):
    """Test suite for User model functionality.

    Tests basic user creation and field validation.
    """

    def test_user(self):
        """Test basic user creation and field values.

        Ensures:
            - User instance is created successfully
            - Username matches expected value
            - Password matches expected value
        """
        u1 = user_example1()
        self.assertTrue(isinstance(u1, User))
        self.assertEqual(u1.username, "your_username")
        self.assertEqual(u1.password, "your_password")


class ProfileModelTests(TestCase):
    """Test suite for Profile model functionality.

    Tests profile creation and its relationship with User model.
    """

    def test_profile(self):
        """Test profile creation and association with user.

        Ensures:
            - Profile is created automatically with user
            - Profile is correctly associated with user
            - Default balance is set to 0
        """
        u1 = user_example1()
        p1 = Profile.objects.get(id=1)
        self.assertTrue(isinstance(p1, Profile))
        self.assertEqual(u1.profile, p1)
        self.assertEqual(p1.balance, 0)
