
from django.shortcuts import render, get_object_or_404
import datetime
from .models import Post

# Create your views here.


def post_list(request):
    post_list = Post.objects.all()
    return render(request, 'blog/posts/list.html', {'post_list': post_list})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    
    return render(request, "blog/posts/detail.html", {'post':post})