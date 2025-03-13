import django_filters
from django_filters import FilterSet
from .models import Post
from django.forms import DateInput

class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок новости содержит:')
    author = django_filters.AllValuesFilter(field_name='author__user__username',label='Автор новости:')
    date = django_filters.DateFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}), label='Дата новости позже:')

    class Meta:
        model = Post
        fields = ['title','author','date']

    # class Meta:
    #     model = Post
    #     fields = {
    #         'title': ['icontains'],
    #         'author__user__username': ['icontains'],
    #         'date': ['gt'],
    #     }