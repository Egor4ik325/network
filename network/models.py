from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse


class Post(models.Model):
    """User post on the website."""
    title = models.CharField(_("Post title"), max_length=50)
    body = models.TextField(_("Post content body"))

    def __str__(self):
        """Model instance string representation."""
        return self.title

    def get_absolute_url(self):
        """Model instance absolute url (reversing URLconf)."""
        return reverse("post", kwargs={"pk": self.pk})
