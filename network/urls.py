from django.urls import path

from .views import IndexView, PostListView, PostDetailView

urlpatterns = [
    path("", IndexView.as_view(), name='index'),

    # Post
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post'),
]
