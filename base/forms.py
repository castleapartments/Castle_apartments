
from django import forms

from django_countries.fields import CountryField
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from cloudinary.forms import CloudinaryJsFileField

from base.models import Card, UserProfile, UserCreditCard


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
    #photo_main = forms.ImageField(widget=forms.widgets.FileInput)
    class Meta:
        model = UserProfile
        #superuser = forms.BooleanField()
        #employee = forms.BooleanField()
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
                'photo_main',
                'description',
            )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save profile'))

class PhotoDirectForm(ProfileForm):
    photo_main = CloudinaryJsFileField()

#class PersonForm(forms.ModelForm):
#    class Meta:
#        model = Person
#        fields = ('name', 'email', 'job_title', 'bio')
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_method = 'post'
#        self.helper.add_input(Submit('submit', 'Save person'))
#
class CreditCardForm(forms.ModelForm):
    class Meta:
        model = UserCreditCard
        fields = ('credit_card_number', 'credit_card_provider', 'credit_card_security_number', 'credit_card_name_on_card','credit_card_expiry')
        widgets = {'credit_card_expiry': forms.DateInput(attrs={'class': 'datetimepicker'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save creditcard'))

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save card'))