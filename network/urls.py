from django.urls import path

from .views import (
    IndexView, PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path("", IndexView.as_view(), name='index'),

    # Post CRUD (display & alter)
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('posts/update/<slug:slug>/',
         PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<slug:slug>/',
         PostDeleteView.as_view(), name='post_delete'),
]
