import tempfile
import shutil
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.core.cache import cache
from django.urls import reverse
from django import forms
from django.conf import settings
from core.slugify.slugify import slugify

from ..models import Post, Group, Comment, Follow

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif')

        cls.user = User.objects.create_user(
            username='автор')
        cls.group = Group.objects.create(
            title='Название группы',
            description='Описание группы')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст поста',
            group=cls.group,
            image=uploaded)
        cls.post = Comment.objects.create(
            text='Текст комментария отображается в post_detail',
            post=cls.post,
            author=cls.user)

        slug = slugify('Название группы')
        urls = [
            reverse('posts:index'),
            reverse('posts:follow_index'),
            reverse('posts:group_list', kwargs={'slug': slug}),
            reverse('posts:profile', kwargs={'username': 'автор'}),
            reverse('posts:post_detail', kwargs={'post_id': 1}),
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            reverse('posts:post_create'),
            'posts/not-exists']

        templates = [
            'posts/index.html',
            'posts/follow.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
            'core/404.html']

        alias = [
            'index',
            'follow_index',
            'group_list',
            'profile',
            'post_detail',
            'post_edit',
            'post_create',
            'not_exits']

        cls.test_data = dict(zip(urls, templates))
        cls.endpoints = dict(zip(alias, urls))
        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def check_post(self, post):
        self.assertIsInstance(post, Post)
        self.assertEqual(post.author.username, 'автор')
        self.assertEqual(post.text, 'Текст поста')
        self.assertEqual(post.group.title, 'Название группы')
        self.assertEqual(post.image, 'posts/small.gif')

    def check_first_post(self, response):
        first_post = response.context['page_obj'][0]
        self.check_post(first_post)

    def check_group(self, group):
        self.assertIsInstance(group, Group)
        self.assertEqual(group.title, 'Название группы')
        self.assertEqual(group.description, 'Описание группы')

    def test_templates(self):
        for reverse_name, template in self.test_data.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_context_index(self):
        response = self.authorized_client.get(self.endpoints['index'])
        self.check_first_post(response)

    def test_context_group_list(self):
        response = self.authorized_client.get(self.endpoints['group_list'])
        self.check_first_post(response)
        self.check_group(response.context['group'])

    def test_context_post_detail(self):
        response = self.authorized_client.get(self.endpoints['post_detail'])
        self.check_post(response.context['post'])

        received = response.context['comments'][0].text
        expected = 'Текст комментария отображается в post_detail'
        self.assertEqual(received, expected)

    def test_context_profile(self):
        response = self.authorized_client.get(self.endpoints['profile'])
        self.check_first_post(response)
        user = response.context['user_obj']
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'автор')

    def test_context_post_create(self):
        response = self.authorized_client.get(self.endpoints['post_create'])
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_context_post_edit(self):
        response = self.authorized_client.get(self.endpoints['post_edit'])

        self.assertTrue(response.context['is_edit'])
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_context_follow(self):
        """
        1. Запись пользователя появляется в ленте тех, кто на него подписан.
        2. Не появляется в ленте тех, кто не подписан.
        """
        # 1 ---
        following_user = User.objects.create_user(username='following автор')
        Follow.objects.create(
            user=following_user,
            author=self.user)

        client = Client()
        client.force_login(following_user)

        response = client.get(self.endpoints['follow_index'])
        self.check_first_post(response)

        # 2 ---
        response = self.authorized_client.get(self.endpoints['follow_index'])
        post_count = len(response.context['page_obj'])
        self.assertEqual(post_count, 0)

    def test_index_cahe(self):
        response1 = self.authorized_client.get(self.endpoints['index'])
        Post.objects.all().delete()
        time.sleep(1)
        response2 = self.authorized_client.get(self.endpoints['index'])
        self.assertEqual(response1.content, response2.content)
        cache.clear()
        response3 = self.authorized_client.get(self.endpoints['index'])
        self.assertNotEqual(response2.content, response3.content)
