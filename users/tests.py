from django.test import TestCase
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class UserModelTests(TestCase):
    """Test custom user model logic/methods."""
    pass


class UserManagerTests(TestCase):
    """Test custom user manager login/creating/deleting."""
    pass


class UserFormTests(TestCase):
    """Test custom user form logic/validating/cleaning."""
    pass


class UserViewTests(TestCase):
    """Test custom user view logic/rendering/templating."""
    pass
