from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from datetime import datetime, timezone, timedelta
from cloudinary.models import CloudinaryField

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

    VALID_FEATURES = (
        ('garage','Garage',
        ('private_entrance',    'Private Entrance')),
        ('elevator',            'Elevator'),
        ('wheelchair_access',   'Wheelchair Access'),
        ('garden',              'Garden'),
        ('animals_allowed',     'Animals Allowed'),
        ('storage',             'Storage'),
        ('shed',                'Shed'),
    )
    features = JSONField(default=list)

    approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(blank=True, null=True)
    featured = models.BooleanField(default=False)

    sold = models.BooleanField(default=False)
    sold_date = models.DateField(null=True, blank=True)

    def populate(self, apartment_form):
        self._populate_features(apartment_form.getlist('features'))

    def _populate_features(self, features):
        valid_features = [t[1] for t in Apartment.VALID_FEATURES]
        self.features = [t for t in features if t in valid_features]



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

    def photo_main(self):
        images = self.images.all().filter(primary=True)
        if images:
            return images[0]
        return None


class ApartmentImages(models.Model):
    apartment_id = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, related_name='images')
    primary = models.BooleanField(default=False)
    image = CloudinaryField(null=True, blank=True)

    def url(self):
        return self.image.url


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
        options = []
        if self.cities:
            options.append('Cities: ({})'.format(','.join([c for c in self.cities])))
        if self.countries:
            options.append('Countries: ({})'.format(','.join([c for c in self.countries])))
        if self.types:
            type_choices = dict(Apartment.TYPE_CHOICES)
            options.append('Types: ({})'.format(','.join([type_choices[c] for c in self.types])))
        if self.min_size or self.max_size:
            options.append('Size: {} to {}'.format(self.min_size if self.min_size else 'Any', self.min_size if self.min_size else 'Any'))
        if self.min_price or self.max_price:
            options.append('Price: {} to {}'.format(self.min_price if self.min_price else 'Any', self.max_price if self.max_price else 'Any'))
        if self.min_rooms or self.max_rooms:
            options.append('Size: {} to {}'.format(self.min_rooms if self.min_rooms else 'Any', self.max_rooms if self.max_rooms else 'Any'))
        if self.street:
            options.append("Street: '{}'".format(self.street))
        if self.description:
            options.append("Description: '{}'".format(self.description))

        if self.age == 'd':
            options.append('Age: 1 Day')
        elif self.age == 'w':
            options.append('Age: 1 Week')
        else:
            options.append('Age: Any')

        return '; '.join(options)

    def history_age(self):
        days_ago = (datetime.now(timezone.utc) - self.created).days
        if days_ago < 1:
            return 'Today'
        elif days_ago < 2:
            return 'Yesterday'
        else:
            return f'{days_ago} days ago'
