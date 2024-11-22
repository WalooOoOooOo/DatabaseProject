from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from Society.models import Society, SocietyAdmin

def forum_page(request):
    query = request.GET.get('q')  
    if query:
        posts = Post.objects.filter(title__icontains=query)  
    else:
        posts = Post.objects.all()  
    
    posts_with_societies = []
    for post in posts:
        author_societies = []
        if post.author.is_authenticated:
            societies = Society.objects.filter(members=post.author) | Society.objects.filter(admins=post.author)
            for society in societies:
                position = "Admin" if society.admins.filter(id=post.author.id).exists() else "Member"
                author_societies.append({'society_name': society.name, 'position': position})
        posts_with_societies.append({'post': post, 'author_societies': author_societies})
    
    return render(request, 'forum.html', {'posts_with_societies': posts_with_societies})


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
    
    user_society_details = None
    if request.user.is_authenticated:
        societies = Society.objects.filter(members=request.user) | Society.objects.filter(admins=request.user)

        user_society_details = []
        for society in societies:
            if society.admins.filter(id=request.user.id).exists():
                position = "Admin"
            else:
                position = "Member"
            user_society_details.append((society.name, position))

    comment_details = []
    for comment in comments:
        comment_society_details = []
        if comment.author.is_authenticated:
            societies = Society.objects.filter(members=comment.author) | Society.objects.filter(admins=comment.author)
            for society in societies:
                if society.admins.filter(id=comment.author.id).exists():
                    position = "Admin"
                else:
                    position = "Member"
                comment_society_details.append((society.name, position))
        comment_details.append({'comment': comment, 'society_details': comment_society_details})

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

    return render(request, 'post_detail.html', {
        'post': post, 
        'comments': comments, 
        'form': form, 
        'user_society_details': user_society_details,
        'comment_details': comment_details
    })

