from django.conf.urls import url
from django.views.generic import ListView, DetailView
from blogengine.models import Post, Category, Tag
from blogengine.views import CategoryListView, TagListView, PostsFeed, getSearchResults, posts_archive, posts_category

urlpatterns = [
    # Index
    url(r'^(?P<page>\d+)?/?$', ListView.as_view(
        model=Post,
        paginate_by=5,
        ),
        name='index'
        ),

    # Individual posts
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Post,
        ),
        name='post'
        ),

    # Categories
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
        model=Category,
        paginate_by=5,
        ),
        name='category'
        ),

    # Tags
    url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
        model=Tag,
        paginate_by=5,
        ),
        name='tag'
        ),

    # Post RSS feed
    url(r'^feeds/posts/$', PostsFeed()),

    # Search posts
    url(r'^search', getSearchResults, name='search'),

    # Archive post
     url(r'^archive/?$', posts_archive, name="post_archive"),

    # Category post
     url(r'^categories/?$', posts_category, name="post_category"),
]
