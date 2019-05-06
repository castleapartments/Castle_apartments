import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')

import django
django.setup()

from faker import Faker
import random
from myfirstapp.models import ApartmentType, ApartmentTypeApartment, ImageApartment, User, SearchHistory, City, Country, Role, Image

fakegen = Faker()

countries = ['Iceland']
cities = ['Reykjavík', "Akureyri", "Egilsstaðir"]

features = ['Balcony', 'Elevator','Available Now', 'Private Shed', 'Garden', 'Private Storage', 'Private Parking', 'Wheelchair Access']
types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family', 'Farms / Land', 'Commercial Property', 'Other']
roles = ['Customer','Agent','Administrator']



def add_country():
    country = Country.objects.get_or_create(countryName=random.choice(countries))[0]
    country.save()
    return country

def add_roles():
    role = Role.objects.get_or_create(roleName=random.choice(roles))[0]
    role.save()
    return role

def populate(n = 5):
    add_roles()
    #for entry in range(n):
    #    fake_name = fakegen.name()
    #    tmp_name = fake_name.split()
    #    fake_first_name = tmp_name[0]
    #    fake_last_name = tmp_name[1]
#
#
    #    firstName
    #    lastName
    #    email
    #    phone
    #    sex
    #    ssn
    #    streetName
    #    streetNumber
    #    postalCode
#
    #    creditCardNumber
    #    creditCardSecurityNumber
    #    creditCardNameOnCard
    #    creditCardExpiry
#
    #    enabled
    #    userCreated
    #    roleID = models.ForeignKey('Role', on_delete=models.CASCADE)
    #    imageID = models.ForeignKey('Image', on_delete=models.CASCADE)
    #    cityID = models.ForeignKey('City', on_delete=models.CASCADE)
    #    countryID = models.ForeignKey('Country', on_delete=models.CASCADE)