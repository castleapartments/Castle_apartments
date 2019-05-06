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