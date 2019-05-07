from django.db import models
from django.contrib.auth.models import User


class Apartment(models.Model):
    apartment_id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    # owner = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)
    # realtor = models.OneToOneField(User, null=True, blank=True, on_delete=models.PROTECT)

    street_name = models.CharField(max_length=100, default='')
    street_number = models.CharField(max_length=10, default='')
    postcode = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')

    size = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True, default='')
    price = models.IntegerField(default=0)

    approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)

    sold = models.BooleanField(default=False)
    sold_date = models.DateField(null=True, blank=True)
    photo_main = models.ImageField(upload_to='image\media', null=True, blank=True)

    def __str__(self):
        return f'{self.street_name} {self.street_number}'
