from django.urls import path
from .views import IndexView

urlpatterns = [
    path('protect/index', IndexView.as_view()),
]