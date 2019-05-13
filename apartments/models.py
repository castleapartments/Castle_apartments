from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import datetime, timezone


class Apartment(models.Model):
    apartment_id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    realtor = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='+')

    street_name = models.CharField(max_length=100, default='')
    street_number = models.CharField(max_length=10, default='')
    postcode = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')

    TYPE_CHOICES = (
            ('apartment',    'Apartment'),
            ('town_house',   'Town House'),
            ('single_family','Single Family House'),
            ('detached',     'Detached'),
            ('summer_house', 'Summer House'),
            ('farm_house',   'Farm House'),
            ('stable',       'Stable'),
            ('garage',       'Garage'),
            ('plot',         'Plot'),
            ('commercial',   'Commercial'),
            ('other',        'Other'),
        )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
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
    photo_main = CloudinaryField(blank=True, null=True)

    def __str__(self):
        return f'{self.street_name} {self.street_number} - {self.postcode} {self.city}'

    @property
    def address(self):
        return f'{self.street_name} {self.street_number}'

    @property
    def location(self):
        return f'{self.postcode} {self.city} ({self.country})'

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

    @property
    def status(self):
        if self.sold:
            return 'Sold'
        if self.approved:
            return 'Approved'
        return 'Pending Approval'


class ApartmentImages(models.Model):
    apartment_id = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE)
    image = CloudinaryField(null=True, blank=True)


class Search(models.Model):
    search_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    min_size = models.IntegerField(null=True)
    max_size = models.IntegerField(null=True)
    min_rooms = models.IntegerField(null=True)
    max_rooms = models.IntegerField(null=True)
    min_price = models.IntegerField(null=True)
    max_price = models.IntegerField(null=True)

    street = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)

    AGE_CHOICES = (
            ('d', '1 Day'),
            ('w', '1 Week'),
        )
    age = models.CharField(
        max_length=1,
        choices=AGE_CHOICES,
        blank=True
    )

    def __str__(self):
        return f'{self.search_id} {self.created} {self.owner} {self.min_size} {self.max_size} {self.min_price} {self.max_price} {self.min_rooms} {self.max_rooms} {self.age}'
