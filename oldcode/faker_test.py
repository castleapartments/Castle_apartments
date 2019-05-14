import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca.settings')
django.setup()
from django.contrib.auth.models import User

from faker import Faker
from faker.providers import credit_card

fakegen = Faker()
fakegen.add_provider(credit_card)

profile = fakegen.profile()
username = profile['username']
password = User.objects.make_random_password()
mail = profile['mail']
company = profile['company']
name = profile['name']
phone_number = fakegen.phone_number()
name_temp = name.split()
first_name = name_temp[0]
last_name = name_temp[1]

sex = profile['sex']
address = profile['address']

city = fakegen.city()
country = fakegen.country()
postalCode = fakegen.postalcode()
streetName = fakegen.street_name()
streetNumber = fakegen.randomize_nb_elements(number=100, le=False, ge=False, min=None, max=None)

creditcard_number = fakegen.credit_card_number()
creditcard_provider = fakegen.credit_card_provider()
creditcard_security = fakegen.credit_card_security_code()
creditcard_expiry = fakegen.date_this_century(before_today=False, after_today=True)



