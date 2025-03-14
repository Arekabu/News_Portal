from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from parameters import *
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        a_posts = Post.objects.filter(author = self)
        a_posts_rating = a_posts.aggregate(Sum('rating'))
        a_comments_rating = Comment.objects.filter(user = self.user).aggregate(Sum('rating'))
        a_posts_comments_rating = Comment.objects.filter(post__in = a_posts).aggregate(Sum('rating'))
        self.rating = a_posts_rating['rating__sum'] * 3 + a_comments_rating['rating__sum'] + a_posts_comments_rating['rating__sum']
        self.save()

class Category(models.Model):
    name = models.CharField(max_length = 255, unique = True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type = models.CharField(max_length = 10, choices = POST_TYPES, default = post)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
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

    def __str__(self):
        return f'{self.title}\n {self.text}'

    def get_absolute_url(self):
        print(self.__dict__)
        # if 'create/' in f'{self.request}':
        #     path = str(self.id)
        # else:
        path = reverse('post_detail', args=[str(self.id)])
        return path

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

    def __str__(self):
        return f'{self.user}\n {self.post}\n {self.text}'