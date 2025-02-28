from django.db import models
from News_Portal.accounts.models import Author
from News_Portal.parameters import POST_TYPES, post
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(unique = True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type = models.CharField(choices = POST_TYPES, default = post)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField()
    text = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124]+'...'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()