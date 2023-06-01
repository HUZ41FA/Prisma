from django.urls import path
from .feeds import LatestPostsFeed
from . import views


app_name = 'blog'

urlpatterns = [
    #path('', view=views.PostListView.as_view(), name='post_list'),
    path('', view=views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', view=views.post_list, name='post_list_by_tag'),
    path('share/<int:post_id>/', view=views.post_share, name='post_share'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
