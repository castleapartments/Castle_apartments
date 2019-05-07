from django import forms
from .models import Apartment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.formMethod = 'post'

        self.helper.layout = Layout(
            Row(
                Column('street_name', css_class='form-group col-md-6 mb-0'),
                Column('street_number', css_class='form-group col-md-6 mb-0')),
            'postcode',
            'city',
            'country',
            'size',
            'rooms',
            'description',
            'price',
            'photo_main',
            Submit('submit', 'Add Apartment')
        )

    class Meta:
        model = Apartment
        fields = ('street_name', 'street_number', 'postcode', 'city', 'country', 'size', 'rooms', 'description', 'price', 'photo_main')
