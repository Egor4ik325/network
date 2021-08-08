from django.test import Client, TestCase
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

from .models import Post


class PostMangerTests(TestCase):
    """Test model instances creation, retrieving and deleting."""

    def test_create_post(self):
        """Test create new post instance."""
        p1 = Post.objects.create(title="Foo title", body="Foo body")
        self.assertTrue(Post.objects.filter(id=p1.id).exists())


class PostModelTests(TestCase):
    """Test model logic (fields & methods)."""
    pass


class PostViewTests(TestCase):
    """Test URLs (view behavior) and response contexts (templates)."""

    def setUp(self):
        """Setup database."""
        p1 = Post.objects.create(title="Foo title", body="Foo body")
        p2 = Post.objects.create(title="Bar title", body="Bar body")
        p3 = Post.objects.create(title="Egg title", body="Egg body")

    def test_posts(self):
        """Test /posts/ URL route."""
        c = Client()
        r = c.get('/posts/')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['posts'].count(), 3)

    def test_valid_post(self):
        """Test /post/<id> URL route (valid id)."""
        p1 = Post.objects.get(id=1)

        c = Client()
        r1 = c.get(f'/posts/{p1.id}/')

        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.context['post'].id, p1.id)

    def test_invalid_post(self):
        """Test /post/<id> URL route (post with such id doesn't exists)."""
        max_id = Post.objects.all().aggregate(Max('id'))['id__max']

        c = Client()
        r = c.get(f'/posts/{max_id + 1}/')

        # Resource not found error
        self.assertEqual(r.status_code, 404)

    def test_create_post(self):
        """Test create post view (GET, POST logic)."""
        c = Client()

        r = c.get('/posts/create/')
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(r.context.get('form'))

        test_data = {'title': 'Bar title', 'body': 'Bar body'}
        r2 = c.post('/posts/create/', data=test_data)
        self.assertEqual(r2.status_code, 302)  # redirect to /posts/
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, test_data['title'])
        self.assertEqual(created_post.body, test_data['body'])
        # Assert redirect location
        self.assertEqual(r2.headers.get('Location'),
                         f'/posts/{created_post.id}/')

    def test_update_post(self):
        """
        Test GET update page with update form.
        Test POST update form data and update post instance.
        """
        c = Client()

        # GET update page with form
        p1 = Post.objects.get(id=1)
        r = c.get(f'/posts/update/{p1.id}/')
        self.assertEqual(r.status_code, 200)

        # POST update data to update model
        test_data = {'title': 'New title', 'body': 'New body'}
        r2 = c.post(f'/posts/update/{p1.id}/', test_data)
        self.assertEqual(r2.status_code, 302)
        updated_post = Post.objects.get(id=1)
        self.assertEqual(updated_post.title, test_data['title'])
        self.assertEqual(updated_post.body, test_data['body'])

    def test_delete_post(self):
        """Test delete confirmation page & view delete logic."""
        c = Client()

        # GET delete confirm page
        p1 = Post.objects.get(id=1)
        r = c.get(f'/posts/delete/{p1.id}/')
        self.assertEqual(r.status_code, 200)

        # POST delete object
        r2 = c.post(f'/posts/delete/{p1.id}/')
        self.assertEqual(r2.status_code, 302)
        self.assertEqual(r2.headers['Location'], '/posts/')
        # Test object is deleted
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(id=p1.id)
