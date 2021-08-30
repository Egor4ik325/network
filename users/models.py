# django.contrib.auth - seperate Django app
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model."""

    followers = models.ManyToManyField("self", related_name="following")

    def clean(self):
        if self in self.followers:
            raise Exception("User cannot follow himself.")

    def get_absolute_url(self):
        """Return user profile url."""
        return reverse("profile", kwargs={"username": self.username})

    def follows(self):
        """Return number of followers."""
        return self.followers.count()
