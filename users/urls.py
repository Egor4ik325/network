from django.urls import path
from django.http import JsonResponse, HttpResponseBadRequest

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # User profile
    path("<username>/profile/", views.UserProfileView.as_view(), name="profile"),
    path("user/detail/", views.UserDetailJSONView.as_view(), name="user_detail"),
    path("<username>/profile/update/", views.UserUpdateView.as_view(), name="user_update"),
    path("get_session_username/", lambda r: JsonResponse({'username': r.user.username}) if r.user.is_authenticated else HttpResponseBadRequest("User are not signed in!"))
]
