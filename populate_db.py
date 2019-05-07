import os
import django
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca.settings')
django.setup()

from django.core.management.base import BaseCommand
from location.models import Country, City
from apartments.models import Apartment, ApartmentFeature, ApartmentType
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.contrib.auth.models import Group


fakegen = Faker()

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

#-------------------------------- IMAGES

#-------------------------------- USERS and PROFILES

#user = User.objects.create_user(username='john',
#                                 email='jlennon@beatles.com',
#                                 password='glass onion')

#my_group = Group.objects.get(name='my_group_name') 
#my_group.user_set.add(your_user)

def create_user(group):
        profile = fakegen.profile()
        username = profile['username']
        password = User.objects.make_random_password()
        mail = profile['mail']
        company = profile['company']
        name = profile['name']
        ssn = profile['ssn']
        phone_number = fakegen.phone_number()
        name_temp = name.split()
        firstname = name_temp[0]
        lastname = name_temp[1]
        
        sex = profile['sex']
        address = profile['address']
        postalCode = fakegen.postalcode()
        streetName = fakegen.street_name()
        streetNumber = fakegen.randomize_nb_elements(number=100, le=False, ge=False, min=None, max=None)
        creditcard_number = fakegen.credit_card_number()
        creditcard_provider = fakegen.credit_card_provider()
        creditcard_security = fakegen.credit_card_security_code()
        creditcard_expiry = fakegen.date_this_century(before_today=False, after_today=True)                     
        user = User.objects.get_or_create(username=username, password=password)
        
        
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group) 
        group.user_set.add(user)
        
        city = fakegen.city()
        country = fakegen.country()
        add_city(city)
        add_country(country)
        city = City.objects.get(cityName=city)
        country = Country.objects.get(countryName=country)

        if city and country and user:
                userprofile = UserProfile.objects.create(
                        user=user, 
                        sex=sex, 
                        firstName=firstname, 
                        lastName=lastname, 
                        email=mail, 
                        phone=phone_number, 
                        ssn=ssn, 
                        streetName=streetName, 
                        streetNumber=streetNumber, 
                        postalCode=postalCode, 
                        creditCardNumber=creditcard_number, 
                        creditCardProvider=creditcard_provider, 
                        creditCardSecurityNumber=creditcard_security, 
                        creditCardNameOnCard=name, 
                        creditCardExpiry=creditcard_expiry, 
                        city=city, 
                        country=country)
                userprofile.save()

def add_user():
        #accounts = User.objects.count()
        employees = User.objects.filter(groups__name='Employee').count()
        administrators = User.objects.filter(groups__name='Administrator').count()
        customers = User.objects.filter(groups__name='Customer').count()

        create_user('Employee')   

        #print(employees)
        #print(administrators)
        #print(customers)
        

#-------------------------------- APARTMENTS and IMAGES



#add_countries()
#add_cities()
#add_features()
#add_types()
add_user()