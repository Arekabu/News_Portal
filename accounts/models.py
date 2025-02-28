from django.db import models
from django.contrib.auth.models import User
from News_Portal.posts.models import Post, Comment

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE())
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        pass
