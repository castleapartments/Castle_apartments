from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Apartment(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)
    apartmentID = models.AutoField(primary_key=True)
    streetName = models.CharField(max_length=50, blank=True, null=True, default='')
    streetNumber = models.IntegerField(blank=True, null=True, default='')
    postalCode = models.IntegerField(blank=True, null=True, default='')
    size = models.IntegerField(blank=True, null=True, default='')
    rooms = models.IntegerField(blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    price = models.IntegerField(blank=True, null=True, default='')
    approved = models.BooleanField()
    sold = models.BooleanField()
    onSaleDate = models.DateField()
    cityID = models.ForeignKey('location.City', on_delete=models.PROTECT)
    countryID = models.ForeignKey('location.Country', on_delete=models.PROTECT)
    registrationDate = models.DateTimeField(auto_now_add=True)

class ApartmentType(models.Model):
    apartmentTypeID = models.AutoField(primary_key=True)
    apartmentTypeName = models.CharField(max_length=50)
    apartmentTypeCreated = models.DateTimeField(auto_now_add=True)

class ApartmentTypeApartment(models.Model):
    apartmentTypeID = models.ForeignKey('ApartmentType', on_delete=models.CASCADE)
    apartmentID = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE)
    apartmentTypeApartmentCreated = models.DateTimeField(auto_now_add=True)

class ApartmentFeature(models.Model):
    apartmentFeatureID = models.AutoField(primary_key=True)
    apartmentFeatureName = models.CharField(max_length=50)
    apartmentFeatureCreated = models.DateTimeField(auto_now_add=True)

class ApartmentFeatureApartment(models.Model):
    apartmentFeatureID = models.ForeignKey('ApartmentFeature', on_delete=models.CASCADE)
    apartmentID = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE)
    apartmentFeatureApartmentCreated = models.DateTimeField(auto_now_add=True)

class ImageApartment(models.Model):
    imageID = models.ForeignKey('image.Image', on_delete=models.CASCADE)
    apartmentID = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE)
    imageApartmentCreated = models.DateTimeField(auto_now_add=True)
