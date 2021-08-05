from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin bound with the Post model."""
    list_display = ('title', 'body')
