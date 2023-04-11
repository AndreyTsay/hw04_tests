
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User
from .forms import PostForm

NUMBER_OF_POSTS: int = 10


def index(request):
    posts = Post.objects.select_related('group', 'author').all()
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "author": author,
        "page_obj": page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_count = post.author.posts.count()
    context = {
        "post": post,
        "post_count": post_count,
    }
    return render(request, "posts/post_detail.html", context)


@login_required(login_url="users:login")
def create_post(request):
    form = PostForm(request.POST or None)
    template = "posts/create_post.html"
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author_id = request.user.id
            instance.save()
            return redirect("posts:profile", request.user)
    return render(request, template, {"form": form})


@login_required(login_url="users:login")
def post_edit(request, post_id):
    template = "posts/create_post.html"
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.user.id != post.author.id:
        return redirect("posts:post_detail", post.pk)
    if request.method == 'POST' and form.is_valid():
        form.save(post)
        return redirect("posts:post_detail", post.id)
    context = {
        "form": form,
        "is_edit": True,
    }
    return render(request, template, context)
