from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='вася')
        cls.post = Post.objects.create(
            text='Пост авторизованного пользователя вася',
            author=cls.user, )
        Group.objects.create(title='user-group')

        cls.user_not_authorized = User.objects.create_user(username='федя')
        cls.post_not_accessible = Post.objects.create(
            text='Пост пользователя федя',
            author=cls.user_not_authorized, )

        cls.public = {
            '/': 'posts/index.html',
            '/group/user-group/': 'posts/group_list.html',
            '/profile/вася/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        cls.authorized = {
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
        }
        cls.end_points = {**cls.public, **cls.authorized}

    def setUp(self):
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

        response = self.authorized_client.get('/posts/2/edit/', follow=True)
        self.assertEqual(
            response.status_code, 403,
            "user(вася) can not access edit-page of other's users post")

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
