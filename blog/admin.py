from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment, Category, Tag


class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ("status", "created_on", "updated_on")
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body', 'post')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ("created_on", 'updated_on')
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ("name",)
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
