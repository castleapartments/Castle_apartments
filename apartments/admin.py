from django.contrib import admin
from .models import Apartment


admin.site.register(Apartment)

#do remove user, updating site settings, admin creations and employee creations also come here as models?