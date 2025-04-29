from django.contrib import admin
from .models import Author, Post, Category, Comment

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'author', 'rating', 'get_categories', 'date']
    list_filter = ('rating', 'date', 'author', 'type', 'category__name')
    search_fields = ('text', 'title')

    def get_categories(self, post):
        return ", ".join([category.name for category in post.category.all()])

    get_categories.short_description = 'Categories'

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('subscribers',)
    search_fields = ('name',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post__title', 'user', 'text', 'rating', 'date']
    list_filter = ('rating', 'date', 'user')
    search_fields = ('text',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
