from django.contrib import admin
from .models import UserProfile, UserProfileImage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserProfileImage)