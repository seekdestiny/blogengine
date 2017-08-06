from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blogengine.models import Category, Post, Tag
from django.contrib.syndication.views import Feed
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
import markdown2

# Create your views here.
class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Post.objects.filter(category=category)
        except Category.DoesNotExist:
            return Post.objects.none()

class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()

class PostsFeed(Feed):
    title = "Jeff Qian's Blog"
    link = '/'
    description = "Jeff Qian's Blog"

    def items(self):
        return Post.objects.order_by('-pub_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        extras = ["fenced-code-blocks"]
        content = mark_safe(markdown2.markdown(force_str(item.text),
                                               extras = extras))
        return content
