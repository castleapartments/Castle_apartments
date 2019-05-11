from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from .models import Apartment
from .forms import ApartmentForm


APARTMENTS_PER_PAGE = 9


class ApartmentManager(object):
    @staticmethod
    def _page(apartments, page):
        paginator = Paginator(apartments, APARTMENTS_PER_PAGE)
        return paginator.get_page(page)

    def get_all(self, page, order='-approval_date'):
        apartments = Apartment.objects.order_by(order).all()
        return self._page(apartments, page)

    def get_featured(self, page):
        featured_apartments = Apartment.objects.all().filter(featured=True)
        if len(featured_apartments) > 0:
            return self._page(featured_apartments, page)
        return self.get_all(page)

    def get_apartment_by_id(self, apartment_id):
        try:
            return Apartment.objects.get(apartment_id=apartment_id)
        except ObjectDoesNotExist:
            return None


apartment_manager = ApartmentManager()


def list_all(request):
    print('list_all')
    order = request.GET.get('order', '-approval_date')
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_all(page, order=order)})


def list_featured(request):
    print('list_featured')
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_featured(page)})


def search(request):
    return render(request, 'apartments/search.html')


def view(request, apartment_id):
    return render(request, 'apartments/view.html', {'apartment': apartment_manager.get_apartment_by_id(apartment_id)})


def add(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()

    form = ApartmentForm()
    return render(request, 'apartments/add.html', {'form': form})
