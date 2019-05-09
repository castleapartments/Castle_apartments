import os
import django
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca.settings')
django.setup()
import random

from django.core.management.base import BaseCommand
from location.models import Country, City
from apartments.models import Apartment
from django.contrib.auth.models import User
from base.models import UserProfile
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
#def add_feature(item):
#    feature = ApartmentFeature.objects.get_or_create(apartmentFeatureName=item)
#    if feature == False:
#        feature.save()
#
#def add_type(item):
#    apartmenttype = ApartmentType.objects.get_or_create(apartmentTypeName=item)
#    if apartmenttype == False:
#        apartmenttype.save()

def add_features():
    for item in features:
        add_feature(item)

def add_types():
    for item in types:
        add_type(item)

#-------------------------------- IMAGES

#-------------------------------- USERS and PROFILES

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

        if city and country and user:
                userprofile = UserProfile.objects.create(
                        user=user, 
                        sex=sex, 
                        first_name=firstname, 
                        last_name=lastname, 
                        email=mail, 
                        phone=phone_number, 
                        ssn=ssn, 
                        street_name=streetName, 
                        street_number=streetNumber, 
                        postal_code=postalCode, 
                        credit_card_number=creditcard_number, 
                        credit_card_provider=creditcard_provider, 
                        credit_card_security_number=creditcard_security, 
                        credit_card_name_on_card=name, 
                        credit_card_expiry=creditcard_expiry, 
                        city=city, 
                        country=country,
                        photo_main="")
                userprofile.save()

def create_users(total, max_total, groupname):
        if total < max_total:
                temp_count = total
                while temp_count < max_total:
                        create_user(groupname)
                        temp_count += 1

def add_user():
        #accounts = User.objects.count()
        total_employees = User.objects.filter(groups__name='Employee').count()
        total_administrators = User.objects.filter(groups__name='Administrator').count()
        total_customers = User.objects.filter(groups__name='Customer').count()

        create_users(total_administrators, 5, "Administrator")
        create_users(total_employees, 15, "Employee")
        create_users(total_customers, 100, "Customer")        

#-------------------------------- APARTMENTS and IMAGES

def add_apartment():
        postcode = fakegen.postalcode()
        street_name = fakegen.street_name()
        street_number = fakegen.randomize_nb_elements(number=100, le=False, ge=False, min=None, max=None)

        city = fakegen.city()
        country = fakegen.country()
        add_city(city)
        add_country(country)
        city = City.objects.get(cityName=city)
        country = Country.objects.get(countryName=country)

        size = random.randint(30, 250)
        rooms = random.randint(2, 5)
        description = fakegen.text()
        price = random.randint(10000000, 100000000)
        approved = fakegen.pybool()
        if approved == True:
                approval_date = fakegen.date_this_month(before_today=True, after_today=False)
        if approved == True:
                sold = fakegen.pybool()
                sold_date = fakegen.date_this_month(before_today=True, after_today=False)
        photo_main = ""

        apartment = Apartment.objects.create(
                street_name = street_name,
                street_number = street_number,
                postcode = postcode,
                city = "",
                country = "",
                size = size,
                rooms = rooms,
                description = description,
                price = price,
                approved = approved,
                approval_date = approval_date,
                sold = sold,
                sold_date = sold_date,
                photo_main = photo_main)
        apartment.save()

add_countries()
add_cities()
#add_features()
#add_types()
add_user()
#add_apartment()