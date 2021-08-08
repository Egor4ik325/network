# django.contrib.auth - seperate Django app
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model."""
    pass
