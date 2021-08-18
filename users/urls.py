from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # User profile
    path("<username>/profile/", views.UserProfileView.as_view(), name="profile"),
    path("user/detail/", views.UserDetailJSONView.as_view(), name="user_detail"),
]
