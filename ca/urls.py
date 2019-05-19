from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

import base.views
from apartments.views import search
from base.views import ProfileDetailView, UserListView, ProfileUpdateView, CreateCreditCardView,\
        ViewCreditCardView, UpdateCreditCardView, SignUpView
import containers.views
import about.views
import apartments.views

urlpatterns = [
    path("", search, name="index"),
    path("users/login/", base.views.user_login, name="login"),
    
    path("forget_password/", base.views.forget_password, name="forget_password"),

    path('change_password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path("users/logout/", base.views.user_logout, name="logout"),
    path("users/signup/", SignUpView.as_view(), name="signup"),
    path('users/', include('django.contrib.auth.urls')),

    path("profile/", base.views.profile, name="profile"),    
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="userprofile_detail"),
    path("profile/<int:pk>/edit", ProfileUpdateView.as_view(), name="userprofile_edit"),

    path("apartments/", include('apartments.urls')),

    path("payment/", base.views.payment, name="payment_page"),
    path("payment/add", CreateCreditCardView.as_view(), name="create_payment_page"),
    path("payment/<int:pk>", ViewCreditCardView.as_view(), name="view_payment_page"),
    path("payment/<int:pk>/edit", UpdateCreditCardView.as_view(), name="view_payment_page"),

    path("admin/", admin.site.urls),

    path('about/', about.views.about_view, name='about'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
