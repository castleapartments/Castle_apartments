from django.db import models
from django.contrib.auth.models import User

from datetime import datetime, timezone

import uuid


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

    type = models.CharField(
        max_length=20,
        choices=(
            ('apartment',    'Apartment'),
            ('detached',     'Detached'),
            ('summer_house', 'Summer House'),
            ('stable',       'Stable'),
            ('Garage',       'Garage'),
            ('plot',         'Plot'),
        ),
        default='apartment'
    )

    size = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    rooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True, default='')
    price = models.IntegerField(default=0)

    approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    featured = models.BooleanField(default=False)

    sold = models.BooleanField(default=False)
    sold_date = models.DateField(null=True, blank=True)
    photo_main = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.street_name} {self.street_number} - {self.postcode} {self.city}'

    @property
    def short_description(self):
        if len(self.description) > 150:
            return self.description[:147] + '...'
        return self.description

    @property
    def age(self):
        if self.approval_date is None:
            return 'Unknown'
        age = datetime.now(timezone.utc) - self.approval_date
        if age.days <= 1:
            return '1 day'
        if age.days < 7:
            return f'{age.days} days'
        if age.days < 14:
            return '1 week'
        return f'{age.days // 7} weeks'

    @property
    def get_price(self):
        return format(self.price, ',')

    def get_size_int(self):
        return int(self.size)


class ApartmentImages(models.Model):
    apartment_id = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE)
    image = models.ImageField()
