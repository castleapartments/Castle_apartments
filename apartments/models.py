from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from datetime import datetime, timezone, timedelta


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
    photo_main = models.ImageField()

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
    image = models.ImageField()


class Search(models.Model):
    search_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    cities = JSONField(default=list)
    countries = JSONField(default=list)
    types = JSONField(default=list)

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

    def populate(self, search_form):
        self._populate_types(search_form.getlist('types'))
        self._populate_countries(search_form.getlist('country'))
        self._populate_cities(search_form.getlist('city'))

    def _populate_types(self, types):
        valid_types = [t[0] for t in Apartment.TYPE_CHOICES]
        self.types = [t for t in types if t in valid_types]

    def _populate_countries(self, countries):
        self.countries = [c for c in countries]

    def _populate_cities(self, cities):
        self.cities = [c for c in cities]

    def filter_location(self, apartments):
        if self.countries:
            query = None
            for country in self.countries:
                if query is None:
                    query = models.Q(country=country)
                else:
                    query = query | models.Q(country=country)
            apartments = apartments.filter(query)
        if self.cities:
            query = None
            for city in self.cities:
                if query is None:
                    query = models.Q(city=city)
                else:
                    query = query | models.Q(city=city)
            apartments = apartments.filter(query)
        return apartments

    def filter_types(self, apartments):
        if self.types:
            query = None
            for type in self.types:
                if query is None:
                    query = models.Q(type=type)
                else:
                    query = query | models.Q(type=type)
            apartments = apartments.filter(query)
        return apartments

    def filter_price(self, apartments):
        if self.min_price:
            apartments = apartments.filter(models.Q(price__gte=self.min_price))
        if self.max_price:
            apartments = apartments.filter(models.Q(price__lte=self.max_price))
        return apartments

    def filter_size(self, apartments):
        if self.min_size:
            apartments = apartments.filter(models.Q(price__gte=self.min_size))
        if self.max_size:
            apartments = apartments.filter(models.Q(price__lte=self.max_size))
        return apartments

    def filter_rooms(self, apartments):
        if self.min_rooms:
            apartments = apartments.filter(models.Q(price__gte=self.min_rooms))
        if self.max_rooms:
            apartments = apartments.filter(models.Q(price__lte=self.max_rooms))
        return apartments

    def filter_age(self, apartments):
        if self.age == 'd':
            one_day_ago = datetime.now() - timedelta(days=1)
            apartments = apartments.filter(models.Q(approval_date__gte=one_day_ago))
        elif self.age == 'w':
            one_week_ago = datetime.now() - timedelta(days=7)
            apartments = apartments.filter(models.Q(approval_date__gte=one_week_ago))
        return apartments

    def filter_street(self, apartments):
        if self.street:
            apartments = apartments.filter(models.Q(street_name__iexact=self.street))
        return apartments

    def filter_description(self, apartments):
        if self.description:
            apartments = apartments.filter(models.Q(description__iexact=self.description))
        return apartments

    def __str__(self):
        s = ''
        s += f'\nsearch_id   : {self.search_id}'
        s += f'\ncreated     : {self.created}'
        s += f'\nowner       : {self.owner}'
        s += f'\ncity        : {self.cities}'
        s += f'\ncountry     : {self.countries}'
        s += f'\ntypes       : {self.types}'
        s += f'\nmin_size    : {self.min_size}'
        s += f'\nmax_size    : {self.max_size}'
        s += f'\nmin_price   : {self.min_price}'
        s += f'\nmax_price   : {self.max_price}'
        s += f'\nmin_rooms   : {self.min_rooms}'
        s += f'\nmax_rooms   : {self.max_rooms}'
        s += f'\nstreet      : {self.street}'
        s += f'\ndescription : {self.description}'
        s += f'\nmax_size    : {self.max_size}'
        s += f'\nage         : {self.age}'
        return s
