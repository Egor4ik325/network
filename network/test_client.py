from django.test import LiveServerTestCase
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
        p1 = Post.objects.create(title="Foo title", body="Foo body")
        p2 = Post.objects.create(title="Bar title", body="Bar body")
        p3 = Post.objects.create(title="Egg title", body="Egg body")

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
        post_ul = self.selenium.find_element_by_id('posts')
        posts = post_ul.find_elements_by_tag_name('li')
        self.assertEqual(len(posts), 3)

    def test_post(self):
        """Assert post.html is rendered correctly."""
        # Asserting post
        p1 = Post.objects.first()

        # Assert valid href URL
        posts_url = f'{self.live_server_url}/posts/'
        self.selenium.get(posts_url)
        post_ul = self.selenium.find_element_by_id('posts')
        posts = post_ul.find_elements_by_tag_name('li')
        a = posts[0].find_element_by_tag_name('a')
        a.click()
        post_url = f'{self.live_server_url}/posts/{p1.id}/'
        self.assertEqual(self.selenium.current_url, post_url)

        # Assert valid HTML DOM
        title = self.selenium.find_element_by_id('title')
        body = self.selenium.find_element_by_id('post-body')
        self.assertEqual(title.text, p1.title)
        self.assertEqual(body.text, p1.body)

    def test_post_create(self):
        """Assert post create form is valid (client-side validation)."""
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
        self.assertRegex(self.selenium.current_url,
                         rf'{self.live_server_url}/posts/\d+/')
        self.assertEqual(Post.objects.count(), 4)
        created_post = Post.objects.last()
        self.assertEqual(created_post.title, title)
        self.assertEqual(created_post.body, body)

    def test_post_update(self):
        """Assert post update form is valid + valid <a>'s href URL."""
        # Testing post
        p1 = Post.objects.first()

        # Assert valid href
        post_url = f'{self.live_server_url}/posts/{p1.id}/'
        self.selenium.get(post_url)
        menu_button = self.selenium.find_element_by_id('menu-button')
        menu_button.click()
        a_post_update = self.selenium.find_element_by_id('post-update')
        a_post_update.click()
        post_create_url = f'{self.live_server_url}/posts/update/{p1.id}/'
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
        self.assertRegex(self.selenium.current_url,
                         rf'{self.live_server_url}/posts/\d+/')
        self.assertEqual(Post.objects.count(), 3)
        updated_post = Post.objects.get(id=p1.id)
        self.assertEqual(updated_post.title, title)
        self.assertEqual(updated_post.body, body)

    def test_post_delete(self):
        """Test that HTML for deleting post is working.
        Assert form validation and submit action."""
        # Testing post
        p1 = Post.objects.first()

        # Assert valid href
        post_url = f'{self.live_server_url}/posts/{p1.id}/'
        self.selenium.get(post_url)
        menu_button = self.selenium.find_element_by_id('menu-button')
        menu_button.click()
        a_post_delete = self.selenium.find_element_by_id('post-delete')
        a_post_delete.click()
        post_delete_url = f'{self.live_server_url}/posts/delete/{p1.id}/'
        self.assertEqual(self.selenium.current_url, post_delete_url)

        # Assert delete confirmation form (submit)
        submit = self.selenium.find_element_by_id('submit-button')
        submit.click()
        self.assertRegex(self.selenium.current_url,
                         f'{self.live_server_url}/posts/')
        self.assertEqual(Post.objects.count(), 2)
