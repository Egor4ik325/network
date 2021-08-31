from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.views.generic.edit import FormMixin
from django.views.generic.list import BaseListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize

from .models import Post
from users.models import CustomUser


class IndexView(TemplateView):
    template_name = "network/index.html"


class PostListView(ListView):
    """Lists posts paginated by 10."""
    template_name = "network/posts.html"

    # MultipleObjectsMixin
    model = Post
    context_object_name = 'posts'
    paginate_by = 10  # context: paginator + page_obj
    ordering = 'date_created'


class PostDetailView(DetailView):
    model = Post
    template_name = "network/post.html"
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name_suffix = "_create"
    fields = ['title', 'body']

    def form_valid(self, form):
        """Override logic when POST form is valid.
        Bind form instance to the request.user."""
        self.object = form.save(commit=False)
        self.object.poster = self.request.user
        self.object.save()

        # Redirect to self.get_success_url()
        return FormMixin.form_valid(self, form)


class OwnerRequiredMixin(UserPassesTestMixin):
    """Owner required feature mixin for UpdateView and DeleteView."""

    permission_denied_message = "You are not allowed to udpate/delete other's post!"

    def test_func(self):
        """Verify user is authenticated and owns requested post (for update/delete)."""
        user = self.request.user
        slug = self.kwargs['slug']
        post = Post.objects.get(slug=slug)
        return user.is_authenticated and post.poster == user


class PostUpdateView(OwnerRequiredMixin, UpdateView):
    model = Post
    template_name_suffix = "_update"
    fields = ['title', 'body']


class PostDeleteView(OwnerRequiredMixin, DeleteView):

    model = Post
    # on GET request
    template_name_suffix = '_confirm_delete'
    context_object_name = 'post'
    # on POST request
    success_url = reverse_lazy('posts')


class PostLikeView(LoginRequiredMixin, View):
    """Switch post like state for current user."""

    def post(self, request, *args, **kwargs):
        """Like/unlike post."""
        post_object = get_object_or_404(Post, slug=self.kwargs['slug'])

        if request.user in post_object.likers.all():
            post_object.likers.remove(request.user)
        else:
            post_object.likers.add(request.user)

        # Response status_code=200
        return HttpResponse()


class UserPostListJSONView(ListView):
    """Respond with all user posts as JSON.

    1. Get objects/queryset by username.
    2. Serialize and return queryset as JSON (not template).
    """
    # Support only GET method
    http_method_names = ['get', ]

    def setup(self, *args, **kwargs):
        """Init username url parametor as attribute."""
        self.username = kwargs['username']

        super().setup(*args, **kwargs)

    def get_queryset(self):
        """Return user's posts queryset."""
        user = get_object_or_404(CustomUser, username=self.username)
        return Post.objects.filter(poster=user)

    def get(self, request, *arg, **kwargs):
        """Return user posts as JSON."""
        queryset = self.get_queryset()
        data = serialize('json', queryset)
        return HttpResponse(content=data, content_type="application/json", status=200)
