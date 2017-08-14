from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.generic import ListView
from blogengine.models import Category, Post, Tag
from django.contrib.syndication.views import Feed
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
import markdown2
import datetime

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

def getSearchResults(request):
    """
    Search for a post by title or text
    """

    #Get the query data
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    #Query the database
    if query:
        results = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
    else:
        results = None

    #Add pagination
    pages = Paginator(results, 5)

    # Get specified page
    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(pages.num_pages)

    # Display the search results
    return render_to_response('blogengine/search_post_list.html',
                              {'page_obj': returned_page,
                               'object_list': returned_page.object_list,
                               'search': query})

def posts_archive(request):
    '''a archive posts listing view'''
    posts = Post.objects.filter().order_by('-pub_date')
    now = datetime.datetime.now()

    #create a dict with the years and months:posts 
    post_dict = {}
    for i in range(posts[0].pub_date.year, posts[len(posts)-1].pub_date.year-1, -1):
        post_dict[i] = {}
        for month in range(1,13):
            post_dict[i][month] = []
    for post in posts:
        post_dict[post.pub_date.year][post.pub_date.month].append(post)
 
    #this is necessary for the years to be sorted
    post_sorted_keys = list(reversed(sorted(post_dict.keys())))
    list_posts = []
    for key in post_sorted_keys:
        adict = {key:post_dict[key]}
        list_posts.append(adict)

    return render_to_response('blogengine/post_archive.html',
                             {'now': now, 'list_posts': list_posts})

def posts_category(request):
    '''a category posts listing view'''
    posts = Post.objects.filter().order_by('-pub_date')
    
    #create a dict with the category and posts
    post_dict = {}
    for post in posts:
        if post.category.name not in post_dict:
            post_dict[post.category.name] = []
        post_dict[post.category.name].append(post)

    return render_to_response('blogengine/post_category.html',
                              {'list_posts': post_dict})
        


