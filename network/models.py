from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.timezone import now


class Post(models.Model):
    """User post on the website."""
    poster = models.ForeignKey("users.CustomUser", verbose_name=_(
        "Post author"), on_delete=models.CASCADE)
    title = models.CharField(_("Post title"), max_length=50)
    body = models.TextField(_("Post content body"))
    slug = models.SlugField(_("Post slug from title"), null=False, unique=True)
    date_created = models.DateField(
        _("Post creation date"), default=now)

    def __str__(self):
        """Model instance string representation."""
        return self.title

    def get_absolute_url(self):
        """Model instance absolute url (reversing URLconf)."""
        return reverse("post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """Prepopulate slug field based on post title."""
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
