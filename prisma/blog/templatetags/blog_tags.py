from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.filter(status="published").count()


@register.inclusion_tag("blog/posts/latest_post.html")
def list_latest_posts(count=5):
    latest_posts = Post.objects.filter(status="published").order_by('-publish')[:count]
    return {"latest_posts":latest_posts}


@register.simple_tag
def most_commented_posts(count=5):
    return Post.objects.filter(status="published").annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))