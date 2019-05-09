
from django import forms

from django_countries.fields import CountryField
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from base.models import Person, Card, UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password')

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.helper = FormHelper()
    #    self.helper.form_method = 'post'
    #    self.helper.add_input(Submit('submit', 'Save person'))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
                'sex',
                'email',
                'phone',
                'ssn',
                'street_name',
                'street_number',
                'postal_code',
                'city',
                'country',
                'photo_main'
            )

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'email', 'job_title', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save card'))

class CustomForm(forms.Form):
    class Meta:
        fields = CountryField().formfield()