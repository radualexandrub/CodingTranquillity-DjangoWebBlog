from django.urls import path
from . import views
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    BlogPostLike,
    UserBlogPostListView,
    robots_txt
)
from django.contrib.sitemaps.views import sitemap
from .sitemaps import BlogPostSitemap, StaticViewSitemap

sitemaps = {
    'posts': BlogPostSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    # path('', views.index, name="index"),
    path('', BlogPostListView.as_view(), name="index"),
    path('user-posts/<username>', UserBlogPostListView.as_view(), name='user-posts'),

    path('blogpost/<int:pk>/',
         BlogPostDetailView.as_view(), name='blogpost-detail'),

    path('blogpost/new/', BlogPostCreateView.as_view(), name='blogpost-create'),

    path('blogpost/<int:pk>/update/',
         BlogPostUpdateView.as_view(), name='blogpost-update'),

    path('blogpost/<int:pk>/delete/',
         BlogPostDeleteView.as_view(), name='blogpost-delete'),

    path('blogpost-like/<int:pk>', views.BlogPostLike, name="blogpost_like"),

    path('about.html', views.about, name="about"),
    path('contact.html', views.contact, name="contact"),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt", robots_txt)
]
