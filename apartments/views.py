from django.shortcuts import render

from .models import Apartment
from .forms import ApartmentForm


class ApartmentListManager(object):
    def get_all(self):
        return Apartment.objects.all()

    def get_featured(self):
        all_apartments = self.get_all()
        featured_apartments = [a for a in all_apartments if a.featured]
        if len(featured_apartments) == 0:
            return all_apartments[:6]
        return featured_apartments


apartment_manager = ApartmentListManager()


def list_all(request):
    context = {
        'apartments': apartment_manager.get_all()
    }
    return render(request, 'apartments/list.html', context)


def list_featured(request):
    context = {
        'apartments': apartment_manager.get_featured()
    }
    return render(request, 'apartments/list.html', context)


def search(request):
    return render(request, 'apartments/search.html')


def view(request):
    return render(request, 'apartments/view.html')


def add(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()

    form = ApartmentForm()
    return render(request, 'apartments/add.html', {'form': form})
