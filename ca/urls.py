from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import base.views
from base.views import PersonListView, PersonCreateView, PersonUpdateView, CardListView, CardUpdateView, CardCreateView, PersonAndCardListView
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", base.views.index, name="index"),
    path("login/", base.views.user_login, name="login"),
    
    path("forget_password/", base.views.forget_password, name="forget_password"),
    path("logout/", base.views.user_logout, name="logout"),
    path("signup/", base.views.signup, name="signup"),
    path("db/", base.views.db, name="db"),
    path("profile/", base.views.profile, name="profile"),
    path("apartments/", include('apartments.urls')),
    path("admin/", admin.site.urls),
    path("pc/", PersonAndCardListView.as_view(),  name="pc_list"),
    path('cards/', CardListView.as_view(), name='card_list'),
    path('cards/<int:pk>/edit/', CardUpdateView.as_view(), name='card_edit'),
    path('cards/add', CardCreateView.as_view(), name='card_add'),
    path('people/', PersonListView.as_view(), name='person_list'),    
    path('people/add/', PersonCreateView.as_view(), name='person_add'),
    path('people/<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
    path("test/", base.views.test, name="test"),
    
]

