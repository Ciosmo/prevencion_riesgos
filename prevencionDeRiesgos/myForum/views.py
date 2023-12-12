
#views for the forum app
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Category, Post
from .utils import update_views
from .forms import ProfilePicUpdateForm

def homeForum(request):
    forums = Category.objects.all()
    context = {
        "forums":forums,
    }
    return render(request, "myForum/home.html", context)

def homeForumDetail(request,slug):

    post = get_object_or_404(Post, slug=slug)
    context = {
        "post": post
    }
    update_views(request, post)

    return render(request, "myForum/detail.html", context)

def homeForumPosts(request,slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    context = {
        "posts": posts,
        "forum": category,
    }
    return render(request, "myForum/posts.html", context)

@login_required
def update_profile_pic(request):
    author = request.user.author
    if request.method == 'POST':
        form = ProfilePicUpdateForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePicUpdateForm(instance=author)