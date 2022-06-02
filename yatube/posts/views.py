from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow


def get_paginator_slice(post_list, request):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    post_list = Post.objects.all().select_related('group')
    page_obj = get_paginator_slice(post_list, request)

    context = {'page_obj': page_obj, 'is_home_page': True}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = get_paginator_slice(post_list, request)

    context = {'group': group, 'page_obj': page_obj}
    return render(request, 'posts/group_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)

    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related('group').filter(author=user_obj)
    page_obj = get_paginator_slice(post_list, request)
    subscribers = user_obj.following.count()

    following = None
    if not request.user.is_anonymous:
        following = user_obj.following.filter(user=request.user).exists()

    context = {
        'page_obj': page_obj,
        'user_obj': user_obj,
        'following': following,
        'subscribers': subscribers}
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author_id = request.user.id
        form.save()
        return redirect('posts:profile', username=request.user.username)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        raise PermissionDenied()

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {'post': post, 'form': form, 'is_edit': True}
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    post = Post.objects.select_related(
        'author'
    ).filter(author__following__user=request.user)
    page_obj = get_paginator_slice(post, request)

    context = {'page_obj': page_obj, 'is_home_page': True}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    user = User.objects.get(username=request.user)

    if user != author:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = User.objects.get(username=request.user)
    author = User.objects.get(username=username)

    Follow.objects.filter(user=user, author=author).delete()
    return redirect('posts:profile', username=username)
