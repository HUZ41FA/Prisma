
from django.shortcuts import render, get_object_or_404
import datetime
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# Create your views here.


def post_list(request):
    post_list = Post.objects.all()
    single_post = Post.objects.get(id=10)
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/posts/list.html', {'post_list': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    
    return render(request, "blog/posts/detail.html", {'post':post})


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'post_list'
    paginate_by = 5
    template_name = "blog/posts/list.html"