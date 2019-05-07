from django.contrib import admin
from .models import Apartment, ApartmentType, ApartmentTypeApartment, ApartmentFeature, ApartmentFeatureApartment, ImageApartment

# Register your models here.
admin.site.register(Apartment)
admin.site.register(ApartmentType)
admin.site.register(ApartmentTypeApartment)
admin.site.register(ApartmentFeature)
admin.site.register(ApartmentFeatureApartment)
admin.site.register(ImageApartment)
#do remove user, updating site settings, admin creations and employee creations also come here as models?