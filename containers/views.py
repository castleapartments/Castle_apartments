from django.shortcuts import render
from .forms import ContainerForm
from .models import Container
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.http import HttpResponse

# Create your views here.
def footer_view(request):
    template_name = 'footer/footer_index.html'
    footer = Container.objects.filter(container_location="footer")
    return render(request, template_name, {'footers': footer})
