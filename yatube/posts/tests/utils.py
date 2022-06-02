from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from ..models import Post, Group, Comment, Follow
from faker import Faker

User = get_user_model()
Faker.seed(0)
fake = Faker()


class Utils:
    @classmethod
    def new_user(cls):
        """new_user() -> User, user_name"""
        user_name = fake.first_name()
        user = User.objects.create_user(user_name)
        return user, user_name

    @classmethod
    def new_post(cls, user, **kwargs):
        """new_post(User) -> Post, text"""
        if not ('text' in kwargs):
            kwargs['text'] = fake.sentence(5)
        post = Post.objects.create(author=user, **kwargs)
        return post, kwargs['text']

    @classmethod
    def new_post_with_img(cls, user, group):
        """new_post_with_img(User, Group) -> Post, text, img"""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        img = 'small.gif'
        uploaded = SimpleUploadedFile(
            name=img,
            content=small_gif,
            content_type='image/gif')
        post, text = cls.new_post(user, group=group, image=uploaded)
        return post, text, img

    @classmethod
    def new_group(cls, **kwargs):
        """new_group() -> Group, title, description"""
        description = fake.sentence(5)[:-1]
        if not ('title' in kwargs):
            kwargs['title'] = fake.sentence(2)[:-1]
        group = Group.objects.create(description=description, **kwargs)
        return group, kwargs['title'], description

    @classmethod
    def new_comment(cls, user, post):
        """new_comment(User, Post) -> text"""
        text = fake.sentence(5)
        Comment.objects.create(author=user, text=text, post=post)
        return text

    @classmethod
    def new_follow(cls, user, author):
        """new_follow(User_logged_in, User_2)"""
        Follow.objects.create(user=user, author=author)
