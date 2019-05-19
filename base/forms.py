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
    #email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) < 1:
            raise forms.ValidationError("Please provide a first name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) < 1:
            raise forms.ValidationError("Please provide a last name")
        return last_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already taken.")
        elif len(email) < 3:
            raise forms.ValidationError("Please provide a valid email!")
        return email 

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

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
        elif UserProfile.objects.filter(ssn=ssn).exists():
            raise forms.ValidationError("Ssn already registered!.")
        return ssn



class ProfileForm(forms.ModelForm):
    #photo_main = forms.ImageField(widget=forms.widgets.FileInput)
    email = forms.EmailField()
    phone = forms.IntegerField()
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
