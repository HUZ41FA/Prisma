from django.contrib import admin
from .models import Post
# Register your models here.


#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created', 'publish')
    list_filter = ('status', 'publish', 'created', 'author')
    search_fields = ('title', 'publish', 'status', 'created')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')