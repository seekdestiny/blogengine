from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
import markdown2 as markdown
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

class PostTest(TestCase):
    def test_create_post(self):
        # Create the post
        post = Post()

        # Set the attributes
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()

        # Save it
        post.save()

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check attributes
        self.assertEqual(only_post.title, 'My first post')
        self.assertEqual(only_post.text, 'This is my first blog post')
        self.assertEqual(only_post.slug, 'my-first-post')
        self.assertEqual(only_post.pub_date.day, post.pub_date.day)
        self.assertEqual(only_post.pub_date.month, post.pub_date.month)
        self.assertEqual(only_post.pub_date.year, post.pub_date.year)
        self.assertEqual(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEqual(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEqual(only_post.pub_date.second, post.pub_date.second)

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

    def test_create_post(self):
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
                'slug': 'my-first-post'
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
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.pub_date = timezone.now()
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
                'slug': 'my-second-post'
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
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
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
    def test_index(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content.decode('utf-8'))
        self.assertTrue(post.pub_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(post.pub_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' \
                in response.content.decode('utf-8'))

    def test_post_page(self):
        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()

        print(post_url)
        # Fetch the post
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content.decode('utf-8'))

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.text) in response.content.decode('utf-8'))

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content.decode('utf-8'))
        self.assertTrue(post.pub_date.strftime('%b') in response.content.decode('utf-8'))
        self.assertTrue(str(post.pub_date.day) in response.content.decode('utf-8'))

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' \
                in response.content.decode('utf-8'))

class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEquals(len(all_pages), 1)
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















