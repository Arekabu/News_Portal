from django import forms
from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = [
           'title',
           'text',
           'author',
           'category',
       ]
       widgets = {
           'category': forms.CheckboxSelectMultiple,
       }
       labels = {
           'title': 'Заголовок:',
           'text': 'Текст:',
           'author': 'Автор:',
           'category': 'Категория:',
       }

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user