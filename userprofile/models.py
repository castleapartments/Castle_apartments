from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):        
    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    sex = models.CharField(max_length=5, default="Male")
    firstName = models.CharField(max_length=50, blank=True, null=True, default='')
    lastName = models.CharField(max_length=50, blank=True, null=True, default='')
    email = models.CharField(max_length=50, blank=True, null=True, default='')
    phone = models.CharField(max_length=50, blank=True, null=True, default='')
    ssn = models.IntegerField(blank=True, null=True, default='')
    streetName = models.CharField(max_length=50, blank=True, null=True, default='')
    streetNumber = models.IntegerField(blank=True, null=True, default='')
    postalCode = models.IntegerField(blank=True, null=True, default='')
    creditCardNumber = models.IntegerField(blank=True, null=True, default='')
    creditCardSecurityNumber = models.IntegerField(blank=True, null=True, default='')
    creditCardNameOnCard = models.CharField(max_length=50, blank=True, null=True, default='')
    creditCardExpiry = models.DateField(blank=True, null=True)
    cityID = models.ForeignKey('location.City', blank=True, null=True, on_delete=models.PROTECT, default='')
    countryID = models.ForeignKey('location.Country', blank=True, null=True, on_delete=models.PROTECT, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName