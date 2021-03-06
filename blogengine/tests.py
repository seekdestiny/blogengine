from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post, Category, Tag
import markdown2 as markdown
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import feedparser
import factory.django
from datetime import datetime
from dateutil import tz

# Factories for tests
class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = (
            'name',
            'domain'
        )
        
    name = 'test.com'
    domain = 'test.com'

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    
    name = 'python'
    description = 'The Python programming language'
    slug = 'python'


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = (
            'name',
            'description',
            'slug'
        )
    
    name = 'perl'
    description = 'The Perl programming language'
    slug = 'perl'


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username','email', 'password',)

    username = 'testuser'
    email = 'user@example.com'
    password = 'password'


class FlatPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlatPage
        django_get_or_create = (
            'url',
            'title',
            'content'
        )

    url = '/about/'
    title = 'About me'
    content = 'All about me'


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = (
            'title',
            'text',
            'slug',
            'pub_date'
        )

    title = 'My first post'
    text = 'This is my first blog post'
    slug = 'my-first-post'
    pub_date = timezone.now()
    author = factory.SubFactory(AuthorFactory)
    site = factory.SubFactory(SiteFactory)
    category = factory.SubFactory(CategoryFactory)

class PostTest(TestCase):
    def test_create_tag(self):
        # Create the tag
        tag = TagFactory()

        # Check we can find it
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEqual(only_tag, tag)

        # Check attributes
        self.assertEqual(only_tag.name, 'perl')
        self.assertEqual(only_tag.description, 'The Perl programming language')

    def test_create_category(self):
        # Create the category
        category = CategoryFactory()

        # Check we can find it
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category, category)

    def test_create_post(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory()

        # Add the tag
        post.tags.add(tag)
        post.save()

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Check attributes
        self.assertEqual(only_post.title, 'My first post')
        self.assertEqual(only_post.text, 'This is my first blog post')
        self.assertEqual(only_post.slug, 'my-first-post')
        self.assertEqual(only_post.site.name, 'test.com')
        self.assertEqual(only_post.site.domain, 'test.com')
        self.assertEqual(only_post.pub_date.day, post.pub_date.day)
        self.assertEqual(only_post.pub_date.month, post.pub_date.month)
        self.assertEqual(only_post.pub_date.year, post.pub_date.year)
        self.assertEqual(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEqual(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEqual(only_post.pub_date.second, post.pub_date.second)
        self.assertEqual(only_post.author.username, 'testuser')
        self.assertEqual(only_post.author.email, 'user@example.com')
        self.assertEqual(only_post.category.name, 'python')
        self.assertEqual(only_post.category.description, 'The Python programming language')

        # Check tags
        post_tags = only_post.tags.all()
        self.assertEqual(len(post_tags), 1)
        only_post_tag = post_tags[0]
        self.assertEqual(only_post_tag, tag)
        self.assertEqual(only_post_tag.name, 'perl')
        self.assertEqual(only_post_tag.description, 'The Perl programming language')

class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/', follow=True)
        # Check response code
        self.assertEqual(response.status_code, 200)
        
        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

        # Log the user in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

    def test_logout(self):
        # Log in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content.decode('utf-8'))

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content.decode('utf-8'))

    def test_create_category(self):
        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Check response code
        response = self.client.get('/admin/blogengine/category/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blogengine/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            }, 
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Edit the category
        response = self.client.post('/admin/blogengine/category/' + str(category.pk) + '/change/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category.name, 'perl')
        self.assertEqual(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Delete the category
        response = self.client.post('/admin/blogengine/category/' + str(category.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 0)

    def test_create_tag(self):
        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Check response code
        response = self.client.get('/admin/blogengine/tag/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new tag
        response = self.client.post('/admin/blogengine/tag/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new tag now in database
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 1)

    def test_edit_tag(self):
        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Edit the tag
        response = self.client.post('/admin/blogengine/tag/' + str(tag.pk) + '/change/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)

        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check tag amended
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEqual(only_tag.name, 'perl')
        self.assertEqual(only_tag.description, 'The Perl programming language')

    def test_delete_tag(self):
        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='jeffqian', password="Qx6y123Y")

        # Delete the tag
        response = self.client.post('/admin/blogengine/tag/' + str(tag.pk) + '/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check tag deleted
        all_tags = Tag.objects.all()
        self.assertEqual(len(all_tags), 0)

    def test_create_post(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Log in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Check response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', 
            {
                'title': 'My first post',
                'text': 'This is my first post',
                'pub_date_0': '2017-07-14',
                'pub_date_1': '22:00:04',
                'slug': 'my-first-post',
                'site': '1',
                'category': str(category.pk),
                'tags': str(tag.pk)
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

    def test_create_post_without_tag(self):
        # Create the category
        category = CategoryFactory()

        # Log in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Check response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', 
            {
                'title': 'My first post',
                'text': 'This is my first post',
                'pub_date_0': '2017-07-14',
                'pub_date_1': '22:00:04',
                'slug': 'my-first-post',
                'site': '1',
                'category': str(category.pk),
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content.decode('utf-8'))

        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

    def test_edit_post(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory()
        post.tags.add(tag)
        post.save()

        # Log in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Edit the post
        response = self.client.post('/admin/blogengine/post/' + str(post.pk) + '/change/', 
            {
                'title': 'My second post',
                'text': 'This is my second blog post',
                'pub_date_0': '2017-07-14',
                'pub_date_1': '22:00:04',
                'slug': 'my-second-post',
                'site': '1',
                'category': str(category.pk),
                'tags': str(tag.pk)
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
      
        # Check changed successfully
        self.assertTrue('changed successfully' in response.content.decode('utf-8'))

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post.title, 'My second post')
        self.assertEqual(only_post.text, 'This is my second blog post')

    def test_delete_post(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory()
        post.tags.add(tag)
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Log in
        self.client.login(username='jeffqian', password='Qx6y123Y')

        # Delete the post
        response = self.client.post('/admin/blogengine/post/' + str(post.pk) + '/delete/', 
            {
                'post': 'yes'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content.decode('utf-8'))

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 0)

class PostViewTest(BaseAcceptanceTest):
    def test_clear_cache(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the first post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Fetch the index
        response = self.client.get(reverse('blogengine:index'))
        self.assertEquals(response.status_code, 200)

        # Create the second post
        post = PostFactory(title='My second post',
                text='This is [my second blog post](http://127.0.0.1:8000/)', 
                slug='my-second-post')
        post.tags.add(tag)

        # Fetch the index again
        response = self.client.get(reverse('blogengine:index'))

        # Check second post present
        self.assertTrue('my second blog post' in response.content.decode('utf-8'))
    
    def test_index(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        post.tags.add(tag)
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Fetch the index
        response = self.client.get(reverse('blogengine:index'))
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content.decode('utf-8'))

        # Check the post tag is in the response
        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content.decode('utf-8'))
        
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('US/Pacific')
        utc = datetime.strptime(post.pub_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)

        # Check the post date is in the response
        self.assertTrue(str(pst.year) in response.content.decode('utf-8'))
        self.assertTrue(pst.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(pst.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' \
                in response.content.decode('utf-8'))

    def test_post_page(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        post.tags.add(tag)
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()

        # Fetch the post
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content.decode('utf-8'))

        # Check the post category is in the response
        self.assertTrue(post.category.name in response.content.decode('utf-8'))

        # Check the post tag is in the response
        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))
        
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('US/Pacific')
        utc = datetime.strptime(post.pub_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)

        # Check the post date is in the response
        self.assertTrue(str(pst.year) in response.content.decode('utf-8'))
        self.assertTrue(pst.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(pst.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' \
                in response.content.decode('utf-8'))

    def test_category_page(self):
        # Create the category
        category = CategoryFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Get the category URL
        category_url = post.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('US/Pacific')
        utc = datetime.strptime(post.pub_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)

        # Check the post date is in the response
        self.assertTrue(str(pst.year) in response.content.decode('utf-8'))
        self.assertTrue(pst.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(pst.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content.decode('utf-8'))

    def test_tag_page(self):
        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create the post
        post = PostFactory(text='This is [my first blog post](http://127.0.0.1:8000/)')
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Get the tag URL
        tag_url = post.tags.all()[0].get_absolute_url()

        # Fetch the tag
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, 200)

        # Check the tag name is in the response
        self.assertTrue(post.tags.all()[0].name in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))
        
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('US/Pacific')
        utc = datetime.strptime(post.pub_date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        pst = utc.astimezone(to_zone)

        # Check the post date is in the response
        self.assertTrue(str(pst.year) in response.content.decode('utf-8'))
        self.assertTrue(pst.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(pst.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content.decode('utf-8'))

    def test_nonexistent_category_page(self):
        category_url = '/category/blah/'
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No posts found' in response.content.decode('utf-8'))

    def test_nonexistent_tag_page(self):
        tag_url = '/tag/blah/'
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('No posts found' in response.content.decode('utf-8'))

class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPageFactory()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEqual(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEqual(only_page, page)

        # Check data correct
        self.assertEqual(only_page.url, '/about/')
        self.assertEqual(only_page.title, 'About me')
        self.assertEqual(only_page.content, 'All about me')

        # Get URL
        page_url = only_page.get_absolute_url()

        # Get the page
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 200)

        # Check title and content in response
        self.assertTrue('About me' in response.content.decode('utf-8'))
        self.assertTrue('All about me' in response.content.decode('utf-8'))

class FeedTest(BaseAcceptanceTest):
    def test_all_post_feed(self):
        # Create the category
        category = CategoryFactory()

        # Create the tag
        tag = TagFactory()

        # Create the author
        author = AuthorFactory()

        # Create the site
        site = SiteFactory()

        # Create a post
        post = PostFactory(text='This is my *first* blog post')

        # Add the tag
        post.tags.add(tag)
        post.save()

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Fetch the feed
        response = self.client.get('/feeds/posts/')
        self.assertEqual(response.status_code, 200)

        # Parse the feed
        feed = feedparser.parse(response.content.decode('utf-8'))

        # Check length
        self.assertEqual(len(feed.entries), 1)

        # Check post retrieved is the correct one
        feed_post = feed.entries[0]
        self.assertEqual(feed_post.title, post.title)
        self.assertTrue('This is my <em>first</em> blog post' in feed_post.description)

class SearchViewTest(BaseAcceptanceTest):
    def test_search(self):
        # Create a post
        post = PostFactory()

        # Create another post
        post2 = PostFactory(text='This is my *second* blog post', 
                            title='My second post',
                            slug='my-second-post')

        # Search for first post
        response = self.client.get(reverse('blogengine:search') + '?q=first')
        self.assertEqual(response.status_code, 200)

        # Check the first post is contained in the results
        self.assertTrue('My first post' in response.content.decode('utf-8'))

        # Check the second post is not contained in the results
        self.assertTrue('My second post' not in response.content.decode('utf-8'))

        # Search for second post
        response = self.client.get(reverse('blogengine:search') + '?q=second')
        self.assertEqual(response.status_code, 200)

        # Check the first post is not contained in the results
        self.assertTrue('My first post' not in response.content.decode('utf-8'))

        # Check the second post is contained in the results
        self.assertTrue('My second post' in response.content.decode('utf-8'))

    def test_failing_search(self):
        # Search for something that is not present
        response = self.client.get(reverse('blogengine:search') + '?q=wibble')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content.decode('utf-8'))

        # Try to get nonexistent second page
        response = self.client.get(reverse('blogengine:search') + '?q=wibble&page=2')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content.decode('utf-8'))














