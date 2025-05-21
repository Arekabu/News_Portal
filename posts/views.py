from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView, View
from django.core.cache import cache
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.utils import timezone
from django.shortcuts import redirect
from .tasks import new_post_notification
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from parameters import news, post
import pytz


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10
    paginate_orphans = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezones'] = pytz.common_timezones
        context['current_time'] = timezone.now()

        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']

        return redirect(request.path)


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_object(self, *args, **kwargs ):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    model = Post
    ordering = '-date'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10
    paginate_orphans = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        categories = self.filterset.data.getlist('category')
        get_cat = ''
        for i in categories:
            if i == categories[0]:
                get_cat += f'category={i}'
            else:
                get_cat += f'&category={i}'
        context['categories'] = get_cat
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        cur_post = form.save(commit=False)
        if 'news/' in f'{self.request}':
            cur_post.type = news
        else:
            cur_post.type = post
        # # cur_post.save()
        #
        # new_post_notification.apply_async(cur_post.pk)

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def subscribe(request):
    user = request.user
    categories = [int(i) for i in request.GET.getlist('category')]
    print_cat = ''
    for c_pk in categories:
        curr_cat = Category.objects.get(id=c_pk)
        curr_cat.subscribers.add(user)
        if c_pk == categories[-1]:
            print_cat += f'\n {curr_cat.name}.'
        else:
            print_cat += f'\n {curr_cat.name},'
    message = f'Вы успешно подписались на следующие категории:{print_cat}'
    print(message)
    return render(request, 'subscribe.html', {'categories':categories, 'message': message})


class Index(View):
    def get(self, request):
        string = _('Привет Мир')

        return HttpResponse(string)
