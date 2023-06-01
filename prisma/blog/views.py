
from django.shortcuts import render, get_object_or_404
import datetime
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentPostForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
# Create your views here.

def post_list(request, tag_slug=None):
    post_list = Post.objects.filter(status="published")
    page = request.GET.get('page')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/posts/list.html', {'post_list': posts, 'page': page, 'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    comment_form = CommentPostForm()
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentPostForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, "blog/posts/detail.html", {'post':post, 'comments':comments, 'comment_form':comment_form, 'new_comment':new_comment, 'similar_posts':similar_posts})

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


    queryset = Post.objects.all()
    context_object_name = 'post_list'
    paginate_by = 5
    template_name = "blog/posts/list.html"

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if request.method != 'POST':
        if 'query' in request.GET:
            form = SearchForm(request.GET)

            if form.is_valid():
                query = form.cleaned_data['query']

                results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)

    return render(request, 'blog/posts/search.html', {'form':form, 'results':results, 'query':query})

