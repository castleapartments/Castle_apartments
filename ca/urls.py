from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

import base.views
from apartments.views import search
from base.views import PersonListView, PersonCreateView, PersonUpdateView,\
        CardListView, CardUpdateView, CardCreateView, PersonAndCardListView,\
        ProfileDetailView, UserListView, ProfileUpdateView, CreateCreditCardView,\
        ViewCreditCardView, UpdateCreditCardView

urlpatterns = [
    path("", search, name="index"),
    path("login/", base.views.user_login, name="login"),
    
    path("forget_password/", base.views.forget_password, name="forget_password"),
    #path("change_password/", auth_views.PasswordChangeForm, name='change_password'),
    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path("logout/", base.views.user_logout, name="logout"),
    path("signup/", base.views.signup, name="signup"),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', UserListView.as_view(), name="user_list"),
    path("profile/", base.views.profile, name="profile"),    
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="userprofile_detail"),
    path("profile/<int:pk>/edit", ProfileUpdateView.as_view(), name="userprofile_edit"),

    path("apartments/", include('apartments.urls')),

    path("payment/", base.views.payment, name="payment_page"),
    path("payment/add", CreateCreditCardView.as_view(), name="create_payment_page"),
    path("payment/<int:pk>", ViewCreditCardView.as_view(), name="view_payment_page"),
    path("payment/<int:pk>/edit", UpdateCreditCardView.as_view(), name="view_payment_page"),

    path("admin/", admin.site.urls),
    path("pc/", PersonAndCardListView.as_view(),  name="pc_list"),
    path('cards/single', base.views.singlecard, name="singlecard"),
    path('cards/', CardListView.as_view(), name='card_list'),
    path('cards/<int:pk>/edit/', CardUpdateView.as_view(), name='card_edit'),
    path('cards/add', CardCreateView.as_view(), name='card_add'),
    path('people/', PersonListView.as_view(), name='person_list'),    
    path('people/add/', PersonCreateView.as_view(), name='person_add'),
    path('people/<int:pk>/edit/', PersonUpdateView.as_view(), name='person_edit'),
    path('avatar/', include('avatar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
