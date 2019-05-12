from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db.models import Q

from .models import Apartment, ApartmentImages
from .forms import ApartmentForm, ApartmentImageForm

from datetime import datetime, timedelta
from collections import namedtuple
import uuid


RangeValue = namedtuple('RangeValue', ['value', 'display'])
APARTMENTS_PER_PAGE = 9
MAX_NUMBER_OF_IMAGES = 12
PRICE_RANGE = [
    RangeValue(0, '0 ISK'),
    RangeValue(5000000, '5 million ISK'),
    RangeValue(10000000, '10 million ISK'),
    RangeValue(15000000, '15 million ISK'),
    RangeValue(20000000, '20 million ISK'),
    RangeValue(25000000, '25 million ISK'),
    RangeValue(30000000, '30 million ISK'),
    RangeValue(35000000, '35 million ISK'),
    RangeValue(40000000, '40 million ISK'),
    RangeValue(50000000, '50 million ISK'),
    RangeValue(60000000, '60 million ISK'),
    RangeValue(70000000, '70 million ISK'),
    RangeValue(80000000, '80 million ISK'),
    RangeValue(90000000, '90 million ISK'),
    RangeValue(100000000, '100 million ISK'),
]
SIZE_RANGE = [
    RangeValue(0, '0 m²'),
    RangeValue(20, '20 m²'),
    RangeValue(40, '40 m²'),
    RangeValue(60, '60 m²'),
    RangeValue(80, '80 m²'),
    RangeValue(100, '100 m²'),
    RangeValue(120, '120 m²'),
    RangeValue(140, '140 m²'),
    RangeValue(160, '160 m²'),
    RangeValue(200, '200 m²'),
    RangeValue(300, '300 m²'),
    RangeValue(500, '500 m²'),
    RangeValue(1000, '1000 m²'),
]
ROOMS_RANGE = [
    RangeValue(1, '1'),
    RangeValue(2, '2'),
    RangeValue(3, '3'),
    RangeValue(4, '4'),
    RangeValue(5, '5'),
    RangeValue(6, '6'),
    RangeValue(8, '8'),
    RangeValue(10, '10'),
]


class SearchResultsBuilder(object):
    def __init__(self, search_dict):
        self._search_dict = dict(search_dict)
        del self._search_dict['csrfmiddlewaretoken']

    def _has_attribute(self, attribute_name):
        return attribute_name in self._search_dict.keys()

    def _get_attribute_value_as_int(self, attribute_name):
        return int(self._search_dict[attribute_name][0])

    def has_types(self):
        return 'types' in self._search_dict.keys()

    def filter_types(self, results):
        if self._has_attribute('types'):
            query = None
            for type in self._search_dict['types']:
                if query is None:
                    query = Q(type=type)
                else:
                    query = query | Q(type=type)
            results = results.filter(query)
        return results

    def filter_price(self, results):
        if self._has_attribute('lower_price'):
            value = self._get_attribute_value_as_int('lower_price')
            results = results.filter(Q(price__gte=value))
        if self._has_attribute('upper_price'):
            value = self._get_attribute_value_as_int('upper_price')
            results = results.filter(Q(price__lte=value))
        return results

    def filter_size(self, results):
        if self._has_attribute('lower_size'):
            value = self._get_attribute_value_as_int('lower_size')
            results = results.filter(Q(size__lte=value))
        if self._has_attribute('upper_size'):
            value = self._get_attribute_value_as_int('upper_size')
            results = results.filter(Q(size__lte=value))
        return results

    def filter_rooms(self, results):
        if self._has_attribute('lower_rooms'):
            value = self._get_attribute_value_as_int('lower_rooms')
            results = results.filter(Q(rooms__lte=value))
        if self._has_attribute('upper_rooms'):
            value = self._get_attribute_value_as_int('upper_rooms')
            results = results.filter(Q(rooms__lte=value))
        return results

    def filter_street(self, results):
        if self._has_attribute('street'):
            value = self._search_dict['street'][0]
            results = results.filter(Q(street_name__iexact=value))
        return results

    def filter_description(self, results):
        if self._has_attribute('description'):
            value = self._search_dict['description'][0]
            results = results.filter(Q(description__iexact=value))
        return results

    def filter_age(self, results):
        if self._has_attribute('age'):
            value = self._search_dict['age'][0]
            if value == '1_day':
                one_day_ago = datetime.now() - timedelta(days=1)
                results = results.filter(Q(approval_date__gte=one_day_ago))
            elif value == '1_week':
                one_week_ago = datetime.now() - timedelta(days=7)
                results = results.filter(Q(approval_date__gte=one_week_ago))
        return results

    # 'types': ['farm_house', 'stable', 'garage'], 'price_from': ['10000000'], 'price_to': ['25000000'], 'address': ['asdf'], 'date': ['any']}>


class ApartmentManager(object):
    def __init__(self):
        self._active_searches = {}

    @staticmethod
    def _page(apartments, page):
        paginator = Paginator(apartments, APARTMENTS_PER_PAGE)
        return paginator.get_page(page)

    def _get_all(self):
        return Apartment.objects.all().filter(approved=True)

    def get_all(self, page, order='-approval_date'):
        apartments = self._get_all().order_by(order)
        return self._page(apartments, page)

    def get_featured(self, page):
        featured_apartments = self._get_all().filter(featured=True)
        if len(featured_apartments) > 0:
            return self._page(featured_apartments, page)
        return self.get_all(page)

    def get_apartment_by_id(self, apartment_id):
        try:
            return Apartment.objects.get(apartment_id=apartment_id)
        except ObjectDoesNotExist:
            return None

    def get_search_results(self, search_dict, page):
        search = SearchResultsBuilder(search_dict)
        apartments = self._get_all()
        apartments = search.filter_types(apartments)
        apartments = search.filter_price(apartments)
        apartments = search.filter_size(apartments)
        apartments = search.filter_rooms(apartments)
        apartments = search.filter_age(apartments)
        apartments = search.filter_street(apartments)
        apartments = search.filter_description(apartments)
        return self._page(apartments, page)


apartment_manager = ApartmentManager()


def list_all(request):
    order = request.GET.get('order', '-approval_date')
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_all(page, order=order)})


def list_featured(request):
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_featured(page)})


def search(request):
    page = request.GET.get('page')
    if request.method == "POST":
        apartments = apartment_manager.get_search_results(request.POST, page)
        context = {
            'search_types'       : Apartment.TYPE_CHOICES,
            'search_prices'      : PRICE_RANGE,
            'search_sizes'       : SIZE_RANGE,
            'search_rooms'       : ROOMS_RANGE,
            'search_results'     : True,
            'apartments'         : apartments,
        }
        return render(request, 'apartments/search.html', context)

    context = {
        'search_types'       : Apartment.TYPE_CHOICES,
        'search_prices'      : PRICE_RANGE,
        'search_sizes'       : SIZE_RANGE,
        'search_rooms'       : ROOMS_RANGE,
        'search_results'     : False,
        'apartments'         : apartment_manager.get_featured(page),
    }
    return render(request, 'apartments/search.html', context)


def view(request, apartment_id):
    images = ApartmentImages.objects.all().filter(apartment_id=apartment_id)
    context = {
        'apartment'  : apartment_manager.get_apartment_by_id(apartment_id),
        'images'     : images,
    }
    return render(request, 'apartments/view.html', context)


@login_required
def add(request):
    #https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
    image_form_set = modelformset_factory(ApartmentImages, form=ApartmentImageForm, extra=MAX_NUMBER_OF_IMAGES)

    if request.method == "POST":
        apartment_form = ApartmentForm(request.POST)
        # image_formset = image_form_set(request.POST, request.FILES, queryset=ApartmentImages.object.none())
        image_formset = image_form_set(request.POST, request.FILES)
        if apartment_form.is_valid() and image_formset.is_valid():
            apartment_object = apartment_form.save(commit=False)
            apartment_object.add_date = datetime.now()
            apartment_object.owner = request.user
            apartment_object.save()

            for form in image_formset.cleaned_data:
                if not form:
                    continue
                image = form['image']
                if not bool(apartment_object.photo_main):
                    apartment_object.photo_main = image
                    apartment_object.save()

                apartment_image = ApartmentImages(apartment_id=apartment_object, image=image)
                apartment_image.save()

            return redirect('view_apartment', apartment_id=apartment_object.apartment_id)
        else:
            print('apartment errors:', apartment_form.errors)
            print('image_formset errors:', image_formset.errors)

    apartment_form = ApartmentForm()
    image_formset = image_form_set(queryset=ApartmentImages.objects.none())
    return render(request, 'apartments/add.html', {'apartment_form': apartment_form, 'image_formset': image_formset})


@login_required
def my(request):
    return render(request, 'apartments/my.html')
