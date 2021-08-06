from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView,
    CreateView, UpdateView, DeleteView,
)

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


class PostCreateView(CreateView):
    model = Post
    template_name_suffix = "_create"
    fields = ['title', 'body']


class PostUpdateView(UpdateView):
    model = Post
    template_name_suffix = "_update"
    fields = ['title', 'body']


class PostDeleteView(DeleteView):
    model = Post
    # on GET request
    template_name_suffix = '_confirm_delete'
    context_object_name = 'post'
    # on POST request
    success_url = reverse_lazy('posts')
