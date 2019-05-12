from django import forms
from .models import Apartment, ApartmentImages
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, Submit


class ApartmentForm(forms.ModelForm):
    street_name = forms.CharField(label="Street Name")
    street_number = forms.CharField(label="Street Number")
    postcode = forms.CharField(label="Postcode")
    city = forms.CharField(label="City")
    country = forms.CharField(label="Country")

    type = forms.CharField(label="Property Type")

    size = forms.DecimalField(label="Size (m²)")
    rooms = forms.IntegerField(label="Number of Roooms")
    bathrooms = forms.IntegerField(label="Number of Bathrooms")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price = forms.IntegerField(label="Price")

    class Meta:
        model = Apartment
        fields = ('street_name', 'street_number', 'postcode', 'city', 'country', 'size', 'type', 'rooms', 'bathrooms', 'description', 'price')


class ApartmentImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = ApartmentImages
        fields = ('image', )
