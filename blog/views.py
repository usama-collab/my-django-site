from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import login


# Create your views here.
def post_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now())
    # posts = Post.objects.all().order_by('-published_date')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, 'blog/post_list.html', stuff_for_frontend)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    stuff_for_frontend = {'post': post}
    # return render(request, 'blog/post_detail.html', {'post': post})
    return render(request, 'blog/post_detail.html', stuff_for_frontend)
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', post.id)
    else:
        form = PostForm()
        stuff_for_frontend = {'form': form}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)
@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save() # we cannot write the commit = True if we want so,because by default save() method have commit = True.
            return redirect('blog:post_detail', post.id)

    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form, 'post': post}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by("-created_date")
    stuff_for_frontend = {'posts': posts}
    return render(request, 'blog/post_draft_list.html', stuff_for_frontend)
@login_required
def post_publish(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.publish()
    return redirect('blog:post_detail', post.id)

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    # return redirect('blog:post_list', post.id) cannot redirect it to url blog:post_list because after deleting the post program again going to find primary_key post.id of that post which is not exist in program after deleting the post so we use a backslash here because it don't check for primary key in return
    return redirect('/', post.id)

@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', post.id)

    else:
        form = CommentForm()
        stuff_for_frontend = {'form': form}
        return render(request, 'blog/add_comment_to_post.html', stuff_for_frontend)
@login_required
def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) 
    comment.delete()
    # return redirect('blog:post_detail', comment.post.id)
    return redirect('blog:post_detail', comment.post.id)

@login_required
def comment_approve(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approve()
    return redirect('blog:post_detail', comment.post.id) #as we know this is reverse view function after something happening on front and so here we cannot return the reverse function by passing comment i.d,we have to return the post i.d to i.t after removing comment from front end,which exactly we do here.


# register

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
        
    else:
        form = UserForm()
    return render(request, 'blog/signup.html', {'form': form})