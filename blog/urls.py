from django.urls import path

from .feeds import LatestPostFeed, AtomSiteNewsFeed

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('feed/rss', LatestPostFeed(), name='post_feed'),
    path('feed/atom', AtomSiteNewsFeed()),
]
