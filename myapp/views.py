from django.shortcuts import render, get_object_or_404, HttpResponse
from django.utils import timezone
from django.shortcuts import redirect

from .models import Post        
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.order_by("-published_date").all() 
    return render(request, 'myapp/posts_list.html', {
        'posts': posts
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myapp/post_detail.html', {
        'post': post
    })

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

        posts = Post.objects.all()
        return render(request, 'myapp/posts_list.html', {'posts':posts})
    else:
        form = PostForm(Post)
        return render(request, 'myapp/post_new.html', {'form': form})

def post_edit(request, pk):
    if request.method == "POST":
        form = request.POST
        post = Post.objects.get(pk=pk)

        post.text = form['text']
        post.published_date = timezone.now()
        post.save()

        posts = Post.objects.all()

        return render(request, 'myapp/posts_list.html', {'posts':posts})

    else:
        post = Post.objects.get(pk=pk)
        post = post
        return render(request, 'myapp/post_edit.html', {'form': post})