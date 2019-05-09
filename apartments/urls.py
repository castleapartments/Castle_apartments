from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list_apartments'),
    path('list', views.list, name='list_apartments'),
    path('search', views.search, name='search_apartments'),
    path('view', views.list, name='view_apartment'),
    path('add', views.add, name='add_apartment'),
]