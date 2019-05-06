import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')
django.setup()

from django.core.management.base import BaseCommand
from location.models import Country, City
from apartments.models import Apartment, ApartmentFeature, ApartmentType

#-------------------------------- COUNTRIES and CITIES

countries = ['Iceland', 'Norway', 'Sweden', 'Denmark']
cities = ['Reykjavík', "Akureyri", "Egilsstaðir"]
def add_country(item):
    country = Country.objects.get_or_create(countryName=item)
    if country == False:
        country.save()

def add_city(item):
    city = City.objects.get_or_create(cityName=item)
    if city == False:
        city.save()

def add_countries():
    for item in countries:
        add_country(item)

def add_cities():
    for item in cities:
        add_city(item)

#-------------------------------- FEATURES and TYPES
features = ['Balcony', 'Elevator','Available Now', 'Private Shed', 'Garden', 'Private Storage', 'Private Parking', 'Wheelchair Access']
types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family', 'Farms / Land', 'Commercial Property', 'Other']
def add_feature(item):
    feature = ApartmentFeature.objects.get_or_create(apartmentFeatureName=item)
    if feature == False:
        feature.save()

def add_type(item):
    apartmenttype = ApartmentType.objects.get_or_create(apartmentTypeName=item)
    if apartmenttype == False:
        apartmenttype.save()

def add_features():
    for item in features:
        add_feature(item)

def add_types():
    for item in types:
        add_type(item)

add_countries()
add_cities()
add_features()
add_types()