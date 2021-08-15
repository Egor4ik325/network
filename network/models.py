from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Post(models.Model):
    """User post on the website."""
    poster = models.ForeignKey("users.CustomUser", verbose_name=_(
        "Post author"), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(_("Post title"), max_length=50)
    body = models.TextField(_("Post content body"))
    slug = models.SlugField(_("Post slug from title"), null=False, unique=True)
    date_created = models.DateField(
        _("Post creation date"), default=now)
    likers = models.ManyToManyField(
        "users.CustomUser",
        verbose_name=_("Post likers"),
        help_text=_("Users who liked this post"),
        related_name='likes'
    )

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

    def clean(self):
        """Custom model validation."""
        # Slug validation
        slug = slugify(self.title)
        if slug in ['create', 'update', 'delete']:
            raise ValidationError({
                'title': _("Post title can't be create/update/delete.")
            })

    def likes(self):
        """Return number of likes under the post."""
        return self.likers.count()
