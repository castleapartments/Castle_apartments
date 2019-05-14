from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('search', views.search),
    path('search/<int:search_id>', views.search_results, name='search_results'),
    path('search/<int:search_id>/delete', views.search_delete, name='search_delete'),
    path('list', views.list_all, name='list_apartments'),
    path('view/<int:apartment_id>', views.view, name='view_apartment'),

    path('add', views.add, name='add_apartment'),
    path('my', views.my, name='my_apartments'),

    path('delete/<int:apartment_id>', views.delete_apartment, name='delete_apartment'),
    path('edit/<int:apartment_id>', views.edit_apartment, name='edit_apartment'),
    path('approve/<int:apartment_id>', views.approve_apartment, name='approve_apartment'),
    path('unapprove/<int:apartment_id>', views.unapprove_apartment, name='unapprove_apartment'),
    path('feature/<int:apartment_id>', views.feature_apartment, name='feature_apartment'),
    path('unfeature/<int:apartment_id>', views.unfeature_apartment, name='unfeature_apartment'),
    path('approve_sale/<int:apartment_id>', views.approve_sale_apartment, name='approve_sale_apartment')
]