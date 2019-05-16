import datetime
from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from kennitala import Kennitala
from cloudinary.forms import CloudinaryJsFileField
from base.models import UserProfile, UserCreditCard
from base.fields import CreditCardField


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password')


class ProfileFormSignup(forms.ModelForm):
    #photo_main = forms.ImageField(widget=forms.widgets.FileInput)
    ssn = forms.CharField()
    class Meta:
        model = UserProfile
        #superuser = forms.BooleanField()
        #employee = forms.BooleanField()
        fields = ('ssn',)

    def clean_ssn(self):
        ssn = self.cleaned_data['ssn']
        Kennitala(ssn).validate()
        if not Kennitala(ssn).validate():
            raise forms.ValidationError("Ssn (kennitala) not correct.")
        return ssn



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

    def clean_ssn(self):
        ssn = self.cleaned_data['ssn']
        Kennitala(ssn).validate()
        if not Kennitala(ssn).validate():
            raise forms.ValidationError("Ssn (kennitala) not correct.")
        return ssn

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save profile'))

class PhotoDirectForm(ProfileForm):
    photo_main = CloudinaryJsFileField()

class CreditCardForm(forms.ModelForm):

    credit_card_number = CreditCardField(placeholder=u'0000 0000 0000 0000', min_length=12, max_length=19)    

    class Meta:
        model = UserCreditCard
        fields = ('credit_card_number', 'credit_card_provider', 'credit_card_security_number', 'credit_card_name_on_card','credit_card_expiry')
        widgets = {'credit_card_expiry': forms.DateInput(attrs={'class': 'datetimepicker'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save creditcard'))

    def clean_credit_card_expiry(self):
        credit_card_expiry = self.cleaned_data['credit_card_expiry']
        if credit_card_expiry < datetime.date.today():
            raise forms.ValidationError("The expiry date cannot be in the past!")
        return credit_card_expiry
