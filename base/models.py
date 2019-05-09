from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Person(models.Model):
    name = models.CharField(max_length=130)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

class Card(models.Model):
    name = models.CharField(max_length=130)

class UserProfile(models.Model):        
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    # required to associate Author model with User model (Important)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    sex = models.CharField(max_length=15, default="Male", choices=SEX_CHOICES)
    email = models.CharField(max_length=150, blank=True, null=True, default='')
    phone = models.CharField(max_length=150, blank=True, null=True, default='')
    ssn = models.CharField(max_length=150, blank=True, null=True, default='', unique=True)
    street_name = models.CharField(max_length=150, blank=True, null=True, default='')
    street_number = models.IntegerField(blank=True, null=True, default=0)
    postal_code = models.IntegerField(blank=True, null=True, default=0)
    
    credit_card_number = models.CharField(max_length=150, blank=True, null=True, default='', unique=True)
    credit_card_provider = models.CharField(max_length=150, blank=True, null=True, default='')
    credit_card_security_number = models.IntegerField(blank=True, null=True, default=0)
    credit_card_name_on_card = models.CharField(max_length=150, blank=True, null=True, default='')
    credit_card_expiry = models.DateField(blank=True, null=True)
    
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')

    photo_main = models.ImageField(null=True, blank=True)
    #city = models.ForeignKey('location.City', blank=True, null=True, on_delete=models.PROTECT, default='')
    #country = models.ForeignKey('location.Country', blank=True, null=True, on_delete=models.PROTECT, default='')

    def __str__(self):
        return self.first_name + " " + self.last_name