from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .models import Apartment, ApartmentImages
from .forms import ApartmentForm, ApartmentImageForm

from datetime import datetime


APARTMENTS_PER_PAGE = 9
MAX_NUMBER_OF_IMAGES = 12


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
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_featured(page)})


def search(request):
    page = request.GET.get('page')
    context = {
        'apartment_types'    : Apartment.TYPE_CHOICES,
        'featured_apartments': apartment_manager.get_featured(page),
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
