from django.test import TestCase

from core.slugify.slugify import slugify
from ..models import Post, Group, User


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='имя')
        cls.post = Post.objects.create(
            text='Пост длинной 23 символа',
            author=cls.user)
        cls.post_short_text = Post.objects.create(
            text='Пост 15 символа',
            author=cls.user)
        cls.group = Group.objects.create(
            title=f'Заголовок группы длинной 101 символов{"_" * 64}',
            description='Описание группы')

    def test_post__str__(self):
        received = str(self.post)
        expected = 'Пост длинной 23...'
        self.assertEqual(
            received,
            expected,
            "Post.__str__ should return first 15 chars of text field + ...")

        received = str(self.post_short_text)
        expected = 'Пост 15 символа'
        self.assertEqual(
            received,
            expected,
            "Post.__str__ should not alter text <= 15 chars")

    def test_group__str__(self):
        received = str(self.group)
        expected = f'Заголовок группы длинной 101 символов{"_" * 64}'
        self.assertEqual(
            received,
            expected,
            "Group.__str__ should return whole title field")

    def test_group_save_method(self):
        received = self.group.slug
        expected = slugify(f'Заголовок группы длинной 101 символов{"_" * 63}')
        self.assertEqual(
            received,
            expected,
            ("Field slug should be transliterated from title "
             "and trimmed to 100 chars by save method"))

    def test_post_verbose_name(self):
        expected_values = {
            'author': 'Автор',
            'group': 'Группа',
            'pub_date': 'Дата публикации',
            'text': 'Текст поста',
        }
        for field_name, expected in expected_values.items():
            with self.subTest(field=field_name):
                received = self.post._meta.get_field(field_name).verbose_name
                self.assertEqual(
                    received,
                    expected,
                    (f"verbose_name on field: '{field_name}' - is missing or "
                     f"it's value doesn't match to: '{expected}'"))

    def test_group_verbose_name(self):
        expected_values = {
            'title': 'Имя группы',
            'slug': 'URL',
            'description': 'Описание',
        }
        for field_name, expected in expected_values.items():
            with self.subTest(field=field_name):
                received = self.group._meta.get_field(field_name).verbose_name
                self.assertEqual(
                    received,
                    expected,
                    (f"verbose_name on field: '{field_name}' - is missing or "
                     f"it's value doesn't match to: '{expected}'"))

    def test_post_help_text(self):
        expected_values = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field_name, expected in expected_values.items():
            with self.subTest(field=field_name):
                received = self.post._meta.get_field(field_name).help_text
                self.assertEqual(
                    received,
                    expected,
                    (f"help_text on field: '{field_name}' - is missing or "
                     f"it's value doesn't match to: '{expected}'"))
