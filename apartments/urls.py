from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_featured, name='apartments'),
    path('list', views.list_all, name='list_apartments'),
    path('search', views.search, name='search_apartments'),
    path('view/<int:apartment_id>', views.view, name='view_apartment'),
    path('add', views.add, name='add_apartment'),
]