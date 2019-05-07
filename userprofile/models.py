from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):        
    SEX_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    sex = models.CharField(max_length=15, default="Male", choices=SEX_CHOICES)
    firstName = models.CharField(max_length=150, blank=True, null=True, default='')
    lastName = models.CharField(max_length=150, blank=True, null=True, default='')
    email = models.CharField(max_length=150, blank=True, null=True, default='')
    phone = models.CharField(max_length=150, blank=True, null=True, default='')
    ssn = models.CharField(max_length=150, blank=True, null=True, default='', unique=True)
    streetName = models.CharField(max_length=150, blank=True, null=True, default='')
    streetNumber = models.IntegerField(blank=True, null=True, default=0)
    postalCode = models.IntegerField(blank=True, null=True, default=0)
    
    creditCardNumber = models.IntegerField(blank=True, null=True, default=0, unique=True)
    creditCardProvider = models.CharField(max_length=150, blank=True, null=True, default='')
    creditCardSecurityNumber = models.IntegerField(blank=True, null=True, default=0)
    creditCardNameOnCard = models.CharField(max_length=150, blank=True, null=True, default='')
    creditCardExpiry = models.DateField(blank=True, null=True)
    
    city = models.ForeignKey('location.City', blank=True, null=True, on_delete=models.PROTECT, default='')
    country = models.ForeignKey('location.Country', blank=True, null=True, on_delete=models.PROTECT, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName

class UserProfileImage(models.Model):
    user = models.ForeignKey('userprofile.UserProfile', on_delete=models.PROTECT)
    image = models.ForeignKey('image.Image', on_delete=models.PROTECT)
    