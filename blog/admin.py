from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment, Category, Tag


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ("status", "created_on", "updated_on")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_on'

    summernote_fields = ('content',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body', 'post')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ("created_on", 'updated_on')
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ("name",)
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}
