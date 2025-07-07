# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Category, Tag
from .forms import PostForm, CommentForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q

def home(request):
    """
    Show paginated list of blog posts with optional filtering and search.
    """
    posts = Post.objects.all().order_by('-created_at')

    # Search query
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()

    # Filter by tag
    tag = request.GET.get('tag')
    if tag:
        posts = posts.filter(tags__icontains=tag)

    # Pagination: 3 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query or '',
        'tag': tag or '',
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, pk):
    """
    Show a single post with comments and form to add a new comment.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to comment.')
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
    """
    Allow authors to create new posts.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save tags
            messages.success(request, 'Post created successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Create Post'})

@login_required
def post_edit(request, pk):
    """
    Allow authors to edit their own posts.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, pk):
    """
    Allow authors to delete their own posts.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')

    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register(request):
    """
    Register new users.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def user_login(request):
    """
    User login view.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html')

@login_required
def user_logout(request):
    """
    Logout user.
    """
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')