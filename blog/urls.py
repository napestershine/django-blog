from django.urls import path

from .feeds import LatestPostFeed, AtomSiteNewsFeed

from . import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>', views.posts_by_category, name='posts_by_category'),
    path('tag/<slug:slug>', views.posts_by_tag, name='posts_by_tag'),
    path('feed/rss', LatestPostFeed(), name='post_feed'),
    path('feed/atom', AtomSiteNewsFeed()),
]
