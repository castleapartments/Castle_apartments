from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
from hello.views import PersonListView, PersonCreateView, PersonUpdateView, CardListView, CardUpdateView, CardCreateView
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("login/", hello.views.login, name="login"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path('cards/', CardListView.as_view(), name='card_list'),
    path('cards/<int:pk>/edit/', CardUpdateView.as_view(), name='card_edit'),
    path('cards/add', CardCreateView.as_view(), name='card_add'),
    path('people/', PersonListView.as_view(), name='person_list'),    
    path('people/add/', PersonCreateView.as_view(), name='person_add'),
    path('people/<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
]
