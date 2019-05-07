from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('list', views.list, name='list'),
    path('search', views.search, name='search'),
    path('view', views.view, name='search'),
    path('add', views.add, name='add'),
]