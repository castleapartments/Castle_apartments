from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Person(models.Model):
    name = models.CharField(max_length=130)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

class Card(models.Model):
    name = models.CharField(max_length=130)

class UserProfile(models.Model):     
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    sex = models.CharField(max_length=15, default="Male", blank=True, null=True, choices=SEX_CHOICES)
    email = models.CharField(max_length=150, blank=True, null=True, default='')
    phone = models.CharField(max_length=150, blank=True, null=True, default='')
    ssn = models.CharField(max_length=150, blank=True, null=True, default='')
    street_name = models.CharField(max_length=150, blank=True, null=True, default='')
    street_number = models.IntegerField(blank=True, null=True, default=0)
    postal_code = models.IntegerField(blank=True, null=True, default=0)
        
    city = models.CharField(max_length=50, default='', blank=True, null=True)
    country = CountryField(blank=True, null=True)

    def __str__(self):
        return "Username : " + self.user.username + " - Name : " +self.user.first_name + " " + self.user.last_name
        

class UserCreditCard(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    credit_card_number = models.CharField(max_length=150, blank=True, null=True, default='', unique=True)
    credit_card_provider = models.CharField(max_length=150, blank=True, null=True, default='')
    credit_card_security_number = models.IntegerField(blank=True, null=True, default=0)
    credit_card_name_on_card = models.CharField(max_length=150, blank=True, null=True, default='')
    credit_card_expiry = models.DateField(blank=True, null=True)

    def __str__(self):
        return "Username : " + self.user.username + " - Name : " +self.user.first_name + " " + self.user.last_name

