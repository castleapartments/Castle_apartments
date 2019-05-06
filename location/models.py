from django.db import models

# Create your models here.
class City(models.Model):
    cityID = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=50, unique=True)
    cityCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cityName

class Country(models.Model):
    countryID = models.AutoField(primary_key=True)
    countryName = models.CharField(max_length=50, unique=True)
    countryCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.countryName