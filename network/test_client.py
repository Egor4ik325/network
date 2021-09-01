from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from re import match

from .models import Post


class PostTemplateTests(LiveServerTestCase):
    """Test client-side code (HTML, JS) - template."""

    @classmethod
    def setUpClass(cls):
        """Setup class fields. Call once before all tests."""
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def setUp(self):
        """Setup database for further testing. Call before every test."""
        # Create test users
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword")
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpassword2")

        # Create test posts
        p1 = Post.objects.create(
            poster=self.user, title="Foo title", body="Foo body")
        p2 = Post.objects.create(
            poster=self.user, title="Bar title", body="Bar body")
        p3 = Post.objects.create(
            poster=self.user2, title="Egg title", body="Egg body")

    @classmethod
    def tearDownClass(cls):
        """Tear down class. Call after all tests."""
        cls.selenium.quit()
        super().tearDownClass()

    def test_posts(self):
        """Assert posts.html template is rendered correctly."""
        # Assert link URL point correctly (test href)
        index_url = self.live_server_url
        self.selenium.get(index_url)
        all_posts_link = self.selenium.find_element_by_link_text('All Posts')
        all_posts_link.click()
        posts_url = f'{self.live_server_url}/posts/'
        self.assertEqual(self.selenium.current_url, posts_url)

        # Assert all posts are rendered (test DOM)
        posts = self.selenium.find_elements_by_class_name('card')
        self.assertEqual(len(posts), 3)

    def test_post(self):
        """Assert post.html is rendered correctly."""
        # Asserting post
        p1 = Post.objects.first()

        # Assert valid href URL
        posts_url = f'{self.live_server_url}/posts/'
        self.selenium.get(posts_url)
        posts = self.selenium.find_elements_by_class_name('card')
        post = posts[0]
        read_link = post.find_element_by_link_text('read')
        read_link.click()
        post_url = f'{self.live_server_url}/posts/{p1.slug}/'
        self.assertEqual(self.selenium.current_url, post_url)

        # Assert valid HTML DOM
        title = self.selenium.find_element_by_id('title')
        body = self.selenium.find_element_by_id('post-body')
        self.assertEqual(title.text, p1.title)
        self.assertEqual(body.text, p1.body)

    def login(self):
        """
        Log client into the account.
        Note: it doesn't perform login/register tests/asserts.
        """
        login_url = f"{self.live_server_url}{reverse('login')}"
        self.selenium.get(login_url)
        username_input = self.selenium.find_element_by_css_selector(
            'input[name=username]')
        password_input = self.selenium.find_element_by_css_selector(
            'input[name=password]')
        submit = self.selenium.find_element_by_css_selector(
            'input[type=submit]')
        username, password = "testuser", "testpassword"
        username_input.send_keys(username)
        password_input.send_keys(password)
        submit.click()

    def logout(self):
        self.selenium.get(reverse('logout'))

    def login2(self):
        """Log-in under second user account."""
        login_url = f"{self.live_server_url}{reverse('login')}"
        self.selenium.get(login_url)
        username_input = self.selenium.find_element_by_css_selector(
            'input[name=username]')
        password_input = self.selenium.find_element_by_css_selector(
            'input[name=password]')
        submit = self.selenium.find_element_by_css_selector(
            'input[type=submit]')
        username, password = "testuser2", "testpassword2"
        username_input.send_keys(username)
        password_input.send_keys(password)
        submit.click()

    def test_post_create(self):
        """Assert post create form is valid (client-side validation)."""
        self.login()

        # Assert valid href URL
        posts_url = f'{self.live_server_url}/posts/'
        self.selenium.get(posts_url)
        a_post_create = self.selenium.find_element_by_id('post-create')
        a_post_create.click()
        post_create_url = f'{self.live_server_url}/posts/create/'
        self.assertEqual(self.selenium.current_url, post_create_url)

        # Assert valid form validation
        title_input = self.selenium.find_element_by_id('id_title')
        body_textarea = self.selenium.find_element_by_id('id_body')
        submit = self.selenium.find_element_by_id('submit_button')
        title = 'Title From Selenium'
        body = 'Body from Selenium'
        title_input.send_keys(title)
        body_textarea.send_keys(body)
        submit.click()
        self.assertEqual(Post.objects.count(), 4)
        created_post = Post.objects.last()
        self.assertRegex(self.selenium.current_url,
                         created_post.get_absolute_url())
        self.assertEqual(created_post.title, title)
        self.assertEqual(created_post.body, body)

    def test_post_update(self):
        """Assert post update form is valid + valid <a>'s href URL."""
        self.login()

        # Testing post
        p1 = Post.objects.first()

        # Assert valid href
        post_url = f'{self.live_server_url}/posts/{p1.slug}/'
        self.selenium.get(post_url)
        menu_button = self.selenium.find_element_by_id('menu-button')
        menu_button.click()
        a_post_update = self.selenium.find_element_by_id('post-update')
        a_post_update.click()
        post_create_url = f'{self.live_server_url}/posts/update/{p1.slug}/'
        self.assertEqual(self.selenium.current_url, post_create_url)

        # Assert update logic from HTML form
        title_input = self.selenium.find_element_by_id('id_title')
        body_textarea = self.selenium.find_element_by_id('id_body')
        submit = self.selenium.find_element_by_id('submit_button')
        title_input.clear()
        body_textarea.clear()
        title = 'New title'
        body = 'New body'
        title_input.send_keys(title)
        body_textarea.send_keys(body)
        submit.click()
        self.assertEqual(Post.objects.count(), 3)
        updated_post = Post.objects.get(id=p1.id)
        self.assertRegex(self.selenium.current_url,
                         updated_post.get_absolute_url())
        self.assertEqual(updated_post.title, title)
        self.assertEqual(updated_post.body, body)

    def test_post_delete(self):
        """Test that HTML for deleting post is working.
        Assert form validation and submit action."""
        self.login()

        # Testing post
        p1 = Post.objects.first()

        # Assert valid href
        post_url = f'{self.live_server_url}/posts/{p1.slug}/'
        self.selenium.get(post_url)
        menu_button = self.selenium.find_element_by_id('menu-button')
        menu_button.click()
        a_post_delete = self.selenium.find_element_by_id('post-delete')
        a_post_delete.click()
        post_delete_url = f'{self.live_server_url}/posts/delete/{p1.slug}/'
        self.assertEqual(self.selenium.current_url, post_delete_url)

        # Assert delete confirmation form (submit)
        submit = self.selenium.find_element_by_id('submit-button')
        submit.click()
        self.assertRegex(self.selenium.current_url,
                         f'{self.live_server_url}/posts/')
        self.assertEqual(Post.objects.count(), 2)

    def test_post_like(self):
        """Assert post liking template + JavaScript is working."""
        self.login()

        # ! Selenium can not get /static/network/ css and js files
        # ! Client-side JavaScript is not working while testing
        self.selenium.get(f'{self.live_server_url}{reverse("posts")}')

        # Testing post
        p1 = Post.objects.first()
        posts = self.selenium.find_elements_by_class_name('card')
        post = posts[0]

        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 0)
        like_icon = post.find_element_by_class_name('like-icon')
        like_icon.click()
        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 1)
        self.selenium.refresh()
        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 1)

        self.logout()
        self.login2()
        self.selenium.get(f'{self.live_server_url}{reverse("posts")}')

        # Testing post
        p1 = Post.objects.first()
        posts = self.selenium.find_elements_by_class_name('card')
        post = posts[0]

        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 1)
        like_icon = post.find_element_by_class_name('like-icon')
        like_icon.click()
        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 2)
        self.selenium.refresh()
        likes_number = int(post.find_element_by_class_name('likes').text)
        self.assertEqual(likes_number, 2)
