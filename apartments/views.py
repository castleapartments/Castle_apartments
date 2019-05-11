from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Apartment
from .forms import ApartmentForm


APARTMENTS_PER_PAGE = 9


class ApartmentManager(object):
    @staticmethod
    def _page(apartments, page):
        paginator = Paginator(apartments, APARTMENTS_PER_PAGE)
        return paginator.get_page(page)

    @staticmethod
    def _get_all():
        return Apartment.objects.all().filter(approved=True)

    def get_all(self, page):
        return self._page(self._get_all(), page)

    def get_featured(self, page):
        all_apartments = self._get_all()
        featured_apartments = [a for a in all_apartments if a.featured]
        if len(featured_apartments) > 0:
            return self._page(featured_apartments, page)
        return self._page(all_apartments, page)

    def get_apartment_by_id(self, apartment_id):
        return self._get_all()[0]

apartment_manager = ApartmentManager()


def list_all(request):
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_all(page)})


def list_featured(request):
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_featured(page)})


def search(request):
    return render(request, 'apartments/search.html')


def view(request, apartment_id):
    context = {
        'apartment': apartment_manager.get_apartment_by_id(apartment_id)
    }
    return render(request, 'apartments/view.html', context)


def add(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()

    form = ApartmentForm()
    return render(request, 'apartments/add.html', {'form': form})
