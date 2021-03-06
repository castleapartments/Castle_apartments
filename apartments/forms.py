from django import forms
from .models import Apartment, ApartmentImages, Search
from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Row, Column, Submit

from cloudinary.forms import CloudinaryJsFileField

class ApartmentForm(forms.ModelForm):
    street_name = forms.CharField(label="Street Name")
    street_number = forms.CharField(label="Street Number")
    postcode = forms.CharField(label="Postcode")
    city = forms.CharField(label="City")
    country = forms.CharField(label="Country")

    type = forms.ChoiceField(label="Property Type", choices=Apartment.TYPE_CHOICES)

    size = forms.DecimalField(label="Size (m²)")
    rooms = forms.IntegerField(label="Number of Roooms")
    bathrooms = forms.IntegerField(label="Number of Bathrooms")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    price = forms.IntegerField(label="Price")
    #features = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple)

    class Meta:
        model = Apartment
        fields = ('street_name', 'street_number', 'postcode', 'city', 'country', 'size', 'type', 'rooms', 'bathrooms', 'description', 'price')

class EditApartmentForm(ApartmentForm):

    class Meta:
        model = Apartment
        fields = ('street_name', 'street_number', 'postcode', 'city', 'country', 'size', 'type', 'rooms', 'bathrooms', 'description', 'price', 'features')



class ApartmentImageForm(forms.ModelForm):
    #image = forms.ImageField(label='Image')
    #image = CloudinaryJsFileField()
    #primary = forms.BooleanField(required=False)
    class Meta:
        model = ApartmentImages
        fields = ('image',)

class PhotoDirectForm(ApartmentImageForm):
    image = CloudinaryJsFileField()

class SearchForm(forms.ModelForm):
    # city = forms.CharField(required=False, max_length=50, default='')
    # country = forms.CharField(required=False, max_length=50, default='')

    min_size = forms.IntegerField(required=False)
    max_size = forms.IntegerField(required=False)
    min_rooms = forms.IntegerField(required=False)
    max_rooms = forms.IntegerField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)

    # street = forms.CharField(required=False, max_length=100, default='')
    # description = forms.CharField(required=False, max_length=100, default='')

    class Meta:
        model = Search
        fields = (
            'min_size',
            'max_size',
            'min_rooms',
            'max_rooms',
            'min_price',
            'max_price',
            'street',
            'description',
            'age'
        )
