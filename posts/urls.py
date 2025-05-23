from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, subscribe, SharedContext
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(PostsList.as_view()), name = 'post_list'),
   path('<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('search', PostSearch.as_view(), name = 'post_search'),
   path('create', PostCreate.as_view(), name = 'post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('subscribe/', subscribe, name='subscribe_me'),
   path('time_zone/', SharedContext.as_view(), name='time_zone'),
]
