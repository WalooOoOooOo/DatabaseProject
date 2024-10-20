from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm

def forum_page(request):
    query = request.GET.get('q')  
    if query:
        posts = Post.objects.filter(title__icontains=query)  
    else:
        posts = Post.objects.all()  
    
    return render(request, 'forum.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            return redirect('forumhome') 
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    comments = post.comments.all()  
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('forumpostdetail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})
