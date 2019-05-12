
from django import forms

from .models import Container

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ('container_name','container_text', 'container_location')