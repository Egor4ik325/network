from django.views.generic import TemplateView, ListView, DetailView

from .models import Post


class IndexView(TemplateView):
    template_name = "network/index.html"


class PostListView(ListView):
    model = Post
    template_name = "network/posts.html"
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = "network/post.html"
    context_object_name = 'post'
