
from django.shortcuts import render, get_object_or_404
import datetime
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

# A class based view "PostListView" is used instead of this
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

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = EmailPostForm()
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            print(cd)

            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            
            send_mail(subject, message, 'admin@myblog.com',
            [cd['to']])

            sent = True

    return render(request, 'blog/posts/share.html', {'form': form, 'post' : post, 'sent':sent})

class PostListView(ListView):

    queryset = Post.objects.all()
    context_object_name = 'post_list'
    paginate_by = 5
    template_name = "blog/posts/list.html"
