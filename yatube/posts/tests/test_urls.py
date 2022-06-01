from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.cache import cache

from .utils import Utils

User = get_user_model()


class PostsURLTests(TestCase, Utils):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user, user_name = cls.new_user()
        cls.new_post(cls.user)
        group, *_ = cls.new_group()

        cls.public = {
            '/': 'posts/index.html',
            f'/group/{group.slug}/': 'posts/group_list.html',
            f'/profile/{user_name}/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        cls.authorized = {
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
        }
        cls.end_points = {**cls.public, **cls.authorized}

    def setUp(self):
        cache.clear()
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    @classmethod
    def get_err_txt(cls, url, code, user=False):
        return (f'\nuser: {"" if user else "not"} authorized'
                f'\nendpoint: {url}'
                f'\nexpected status code: 200'
                f'\nactual status code: {code}\n')

    def test_status_code_authorized(self):
        for url in self.end_points.keys():
            with self.subTest(url=url):
                code = self.authorized_client.get(url).status_code
                self.assertEqual(code, 200, self.get_err_txt(url, code, True))

        user_2, _ = self.new_user()
        post_2, _ = self.new_post(user_2)
        url_2 = f'/posts/{post_2.pk}/edit/'
        response = self.authorized_client.get(url_2, follow=True)
        self.assertEqual(response.status_code, 403,
                         "user can not access edit-page of other's users")

    def test_status_code_not_authorized(self):
        for url in self.public.keys():
            with self.subTest(url=url):
                code = self.guest_client.get(url).status_code
                self.assertEqual(code, 200, self.get_err_txt(url, code))

    def test_status_code_not_authorized_redirect(self):
        for url in self.authorized.keys():
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={url}')

        comment_url = '/posts/1/comment/'
        response = self.guest_client.get(comment_url, follow=True)
        self.assertRedirects(response, f'/auth/login/?next={comment_url}')

    def test_templates(self):
        for url, template in self.end_points.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(
                    response,
                    template,
                    (f'\nexpected template: {template} in:'
                     f'\nreceived templates: '
                     f'{[t.name for t in response.templates]}\n'))
