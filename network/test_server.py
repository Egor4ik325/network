from django.test import Client, TestCase
from django.urls import reverse
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model

from .models import Post


class PostModelManagerTests(TestCase):
    """Test model instances creation, retrieving and deleting."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword")

    def test_create_post(self):
        """Test create new post instance."""
        p1 = Post.objects.create(
            poster=self.user, title="Foo title", body="Foo body")
        created_post = Post.objects.get(id=p1.id)
        self.assertEqual(created_post.slug, 'foo-title')


class PostModelTests(TestCase):
    """Test model logic (fields & methods)."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpassword2")
        self.user3 = get_user_model().objects.create_user(
            username="testuser3", password="testpassword3")
        self.user4 = get_user_model().objects.create_user(
            username="testuser4", password="testpassword4")

    def test_post_validation(self):
        """Test Post model data validation."""
        p1 = Post(poster=self.user, title="create",
                  body="Post with invalid title")
        p2 = Post(poster=self.user, title="update",
                  body="Post with invalid title")
        p3 = Post(poster=self.user2, title="delete",
                  body="Post with invalid title")

        # Assert raise ValidationError
        with self.assertRaises(ValidationError):
            p1.full_clean()
            p2.full_clean()
            p3.full_clean()

    def test_post_likes(self):
        """Assert likers field RelatedManager is working OK."""
        p1 = Post.objects.create(poster=self.user, title="Post by first user",
                                 body="This is my first post!")
        p2 = Post.objects.create(poster=self.user2, title="Post by second user",
                                 body="This is my first post!")
        p3 = Post.objects.create(poster=self.user3, title="Post by third user",
                                 body="This is my first post!")
        p4 = Post.objects.create(poster=self.user4, title="Post by forth user",
                                 body="This is my first post!")

        p1.likers.add(self.user2, self.user3)
        p2.likers.add(self.user, self.user4)
        p3.likers.add(self.user, self.user2, self.user3)
        p4.likers.add(self.user2)

        self.assertEqual(self.user.likes.count(), 2)
        self.assertEqual(self.user2.likes.count(), 3)
        self.assertEqual(self.user3.likes.count(), 2)
        self.assertEqual(self.user4.likes.count(), 1)


class PostModelFormTests(TestCase):
    pass


class PostViewTests(TestCase):
    """Test URLs (view behavior) and response contexts (templates)."""

    @classmethod
    def setUpClass(cls):
        """Setup for all tests (common setup)."""
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword")
        cls.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpassword2")
        cls.c = Client()

    def setUp(self):
        """Set up database before every test."""
        p1 = Post.objects.create(
            poster=self.user, title="Foo title", body="Foo body")
        p2 = Post.objects.create(
            poster=self.user, title="Bar title", body="Bar body")
        p3 = Post.objects.create(
            poster=self.user2, title="Egg title", body="Egg body")

    def test_posts(self):
        """Test /posts/ URL route."""
        r = self.c.get('/posts/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['posts'].count(), 3)

    def test_valid_post(self):
        """Test /post/<id> URL route (valid id)."""
        p1 = Post.objects.first()

        r1 = self.c.get(f'/posts/{p1.slug}/')
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.context['post'].id, p1.id)

    def test_invalid_post(self):
        """Test /post/<slug> URL route (slug doesn't exists)."""
        new_slug = 'something-similar-to-slug'

        r = self.c.get(f'/posts/{new_slug}/')
        # Resource not found error
        self.assertEqual(r.status_code, 404)

    def test_create_post(self):
        """Test create post view (GET, POST logic)."""
        self.c.login(username="testuser", password="testpassword")

        r = self.c.get('/posts/create/')
        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(r.context.get('form'))

        test_data = {'title': 'Boom title', 'body': 'Boom body'}
        r2 = self.c.post('/posts/create/', data=test_data)
        self.assertEqual(r2.status_code, 302)  # redirect to /posts/
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, test_data['title'])
        self.assertEqual(created_post.body, test_data['body'])
        # Assert redirect location
        self.assertEqual(r2.headers.get('Location'),
                         f'/posts/{created_post.slug}/')

    def test_create_post_login_required(self):
        """Test user should be authenticated to create posts."""
        r = self.c.get(reverse('post_create'))
        self.assertEqual(r.status_code, 302)
        self.assertRegex(r.headers['Location'], reverse('login'))

    def test_update_post(self):
        """
        Test GET update page with update form.
        Test POST update form data and update post instance.
        """
        self.c.login(username="testuser", password="testpassword")

        # GET update page with form
        p1 = Post.objects.first()
        r = self.c.get(f'/posts/update/{p1.slug}/')
        self.assertEqual(r.status_code, 200)

        # POST update data to update model
        test_data = {'title': 'New title', 'body': 'New body'}
        r2 = self.c.post(f'/posts/update/{p1.slug}/', test_data)
        self.assertEqual(r2.status_code, 302)
        updated_post = Post.objects.first()
        self.assertEqual(updated_post.title, test_data['title'])
        self.assertEqual(updated_post.body, test_data['body'])

    def test_update_post_login_required(self):
        """Test user should be authenticated to update any posts."""
        p1 = Post.objects.first()
        r = self.c.get(reverse('post_update', kwargs={'slug': p1.slug}))
        self.assertEqual(r.status_code, 302)
        self.assertRegex(r.headers['Location'], reverse('login'))

    def test_update_post_owner_required(self):
        """Test user should be owner to update posts."""
        self.c.login(username="testuser", password="testpassword")
        p3 = Post.objects.last()
        r = self.c.get(reverse('post_update', kwargs={'slug': p3.slug}))
        # Access forbidden
        self.assertEqual(r.status_code, 403)

    def test_delete_post(self):
        """Test delete confirmation page & view delete logic."""
        self.c.login(username="testuser", password="testpassword")

        # GET delete confirm page
        p1 = Post.objects.first()
        r = self.c.get(f'/posts/delete/{p1.slug}/')
        self.assertEqual(r.status_code, 200)

        # POST delete object
        r2 = self.c.post(f'/posts/delete/{p1.slug}/')
        self.assertEqual(r2.status_code, 302)
        self.assertEqual(r2.headers['Location'], '/posts/')
        # Test object is deleted
        with self.assertRaises(ObjectDoesNotExist):
            Post.objects.get(id=p1.id)

    def test_delete_post_login_required(self):
        """Test user should be authenticated to delete any posts."""
        p1 = Post.objects.get(id=1)
        r = self.c.get(reverse('post_delete', kwargs={'slug': p1.slug}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.headers['Location'], reverse('login'))

    def test_delete_post_login_required(self):
        """Test user should be owner to update posts."""
        self.c.login(username="testuser", password="testpassword")
        p3 = Post.objects.all()[2]
        r = self.c.get(reverse('post_delete', kwargs={'slug': p3.slug}))
        # Access forbidden
        self.assertEqual(r.status_code, 403)


# class PostLikeView(LoginRequiredMixin, View):
#     """Switch post like state for current user."""

#     def post(self, request, *args, **kwargs):
#         """Like/unlike post."""
#         post_object = get_object_or_404(Post, slug=self.kwargs['slug'])

#         if request.user in post_object.likers.all():
#             post_object.likers.remove(request.user)
#         else:
#             post_object.likers.add(request.user)

#         # Response status_code=200
#         return HttpResponse()


    def test_like_post_login(self):
        """Assert like view/API is requiring login."""
        # Post for testing like func.
        p1 = Post.objects.first()
        self.assertEqual(p1.likes(), 0)
        r1 = self.c.post(reverse('post_like', kwargs={'slug': p1.slug}))
        self.assertEqual(r1.status_code, 302)

    def test_like_post_405(self):
        """Assert like view/API requires POST."""
        self.c.login(username="testuser", password="testpassword")

        # Post for testing like func.
        p1 = Post.objects.first()
        self.assertEqual(p1.likes(), 0)
        r = self.c.put(reverse('post_like', kwargs={'slug': p1.slug}))
        self.assertEqual(r.status_code, 405)
        r = self.c.get(reverse('post_like', kwargs={'slug': p1.slug}))
        self.assertEqual(r.status_code, 405)

    def test_like_post(self):
        """Assert like view/API is working."""
        self.c.login(username="testuser", password="testpassword")

        # Post for testing like func.
        p1 = Post.objects.first()
        self.assertEqual(p1.likes(), 0)
        r1 = self.c.post(reverse('post_like', kwargs={'slug': p1.slug}))
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(p1.likes(), 1)
        r2 = self.c.post(reverse('post_like', kwargs={'slug': p1.slug}))
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(p1.likes(), 0)
        r3 = self.c.post(reverse('post_like', kwargs={
            'slug': 'non-existing-slug'}))
        self.assertEqual(r3.status_code, 404)
