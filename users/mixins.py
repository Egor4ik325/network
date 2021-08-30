from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsnotUserMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated.
    And isn't trying to make action on himself (e.g. follow)."""

    def test_func(self):
        return self.request.user.is_authenticated and self.kwargs.get('username') != self.request.user.username
