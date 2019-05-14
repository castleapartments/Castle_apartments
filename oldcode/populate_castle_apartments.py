import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')

import django
django.setup()

from faker import Faker
import random
#from .models import ApartmentType, ApartmentTypeApartment, ImageApartment, UserProfile, SearchHistory, City, Country, Image
from .models import Country

fakegen = Faker()

countries = ['Iceland']
cities = ['Reykjavík', "Akureyri", "Egilsstaðir"]

features = ['Balcony', 'Elevator','Available Now', 'Private Shed', 'Garden', 'Private Storage', 'Private Parking', 'Wheelchair Access']
types = ['Single Family', 'Condo', 'Townhouse', 'Multi-Family', 'Farms / Land', 'Commercial Property', 'Other']
roles = ['Customer','Agent','Administrator']


def add_country():
    for item in countries:
        country = Country(countryName=item)
        country.save()



def populate(n = 5):
    add_country()
    #add_cities()
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

def main():
    populate(1)

if __name__ == "__main__":
    main()
    