# myForum/urls.py

from django.urls import path
from .views import homeForum, homeForumDetail, homeForumPosts

urlpatterns = [
    path('home/', homeForum, name='homeForum'),
    path('detail/<slug>/', homeForumDetail, name='homeForumDetail'),
    path('posts/<slug>/', homeForumPosts, name='homeForumPosts'),
]