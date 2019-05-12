from django.db import models

class City(models.Model):
    city_name = models.CharField(max_length=130)
    city_postal_code = models.IntegerField(blank=True)
    city_zip = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.city_name)