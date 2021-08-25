# django.contrib.auth - seperate Django app
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model."""

    def get_absolute_url(self):
        """Return user profile url."""
        return reverse("profile", kwargs={"username": self.username})
    
