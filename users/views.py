import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.urls import reverse
from django.core import serializers
from django.views import View
from django.views.generic import TemplateView, UpdateView

from .models import CustomUser


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "users/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "users/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html")


class UserProfileView(TemplateView):
    """View for displaying empty profile web page
    for further client-side rendering."""

    template_name = 'users/profile.html'

    # TODO: add kwargs.username validation before returning template (HTTP 404)


class UserDetailJSONView(View):
    """View for rendering (on the client) information about the user."""

    def get(self, request, *args, **kwargs):
        """Return serialized user model in JSON format."""
        # Get username from query string (payload)
        username = request.GET.get('username')

        if username is None:
            return HttpResponseBadRequest("Username argument in required")

        user = get_object_or_404(get_user_model(), username=username)
        data = serializers.serialize('json', [user], fields=(
            'username', 'first_name', 'last_name', 'email', 'date_joined'))
        return JsonResponse(data=data, safe=False)

class UserIsUserMixin(UserPassesTestMixin):
    """Validate user is requesting user for update/delete."""

    permission_denied_message = "You are not allowed to update/delete other users!"

    def test_func(self):
        """Verify user is authenticated and is requested user (for update/delete)."""
        user = self.request.user
        username = self.kwargs['username']
        user2 = CustomUser.objects.get(username=username)
        return user.is_authenticated and user == user2

class UserUpdateView(UserIsUserMixin, UpdateView):
    """
    View for updating information about the user.

    GET: Return bound/filled HTML form for updating user.
    POST: Process data and update user model.
    """
    template_name = 'users/update_form.html'
    fields = ['first_name', 'last_name', 'email', 'username']
    context_object_name = 'updating_user'

    # From SingleObjectMixin.get_object
    def get_object(self, queryset=None):
        """
        Return the user the view is displaying for update.
        """
        try:
            # Look up object by username
            username = self.kwargs.get('username')
            obj = CustomUser.objects.get(username=username)
        except queryset.model.DoesNotExist:
            raise Http404(_("No users with username: %(username)s") % {'username': username})
        return obj
    
    