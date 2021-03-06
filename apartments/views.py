from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden

from .models import Apartment, ApartmentImages, Search
from .forms import ApartmentForm, ApartmentImageForm, SearchForm, EditApartmentForm
from base.models import UserProfile, UserCreditCard

from datetime import datetime, time
from collections import namedtuple


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
ORDER_CHOICES = ['price', '-price', 'size', '-size', 'approval_date', '-approval_date']

class SearchManager(object):
    def __init__(self, apartment_manager):
        self._apartment_manager = apartment_manager
    @staticmethod
    def _get_all():
        return Search.objects.all()

    @staticmethod
    def get_by_id(search_id):
        return Search.objects.get(search_id=search_id)

    def get_results(self, search_object):
        apartments = self._apartment_manager.get_approved()
        apartments = search_object.filter_location(apartments)
        apartments = search_object.filter_types(apartments)
        apartments = search_object.filter_price(apartments)
        apartments = search_object.filter_size(apartments)
        apartments = search_object.filter_rooms(apartments)
        apartments = search_object.filter_age(apartments)
        apartments = search_object.filter_street(apartments)
        apartments = search_object.filter_description(apartments)
        return apartments

    def get_owners_searches(self, owner):
        return self._get_all().filter(owner=owner)


class ApartmentManager(object):
    def __init__(self):
        self._active_searches = {}

    @staticmethod
    def paginate(apartments, page):
        paginator = Paginator(apartments, APARTMENTS_PER_PAGE)
        return paginator.get_page(page)

    @staticmethod
    def _get_all():
        return Apartment.objects.all()

    def get_approved(self):
        return self._get_all().filter(approved=True)

    def get_unapproved(self):
        return self._get_all().filter(approved=False)

    def get_all(self, page, order='-approval_date'):
        apartments = self.get_approved().order_by(order)
        return self.paginate(apartments, page)

    def get_featured(self, page, order='-approval_date'):
        print(order)
        featured_apartments = self.get_approved().filter(featured=True).order_by(order)
        if len(featured_apartments) > 0:
            return self.paginate(featured_apartments, page)
        return self.get_all(page, order)

    @staticmethod
    def get_by_id(apartment_id):
        try:
            return Apartment.objects.get(apartment_id=apartment_id)
        except ObjectDoesNotExist:
            return None

    def build_country_city_dict(self):
        all_apartments = self.get_approved()
        all_countries = set([a.country for a in all_apartments])
        country_city_dict = dict(((c, set()) for c in all_countries))

        for country, cities in country_city_dict.items():
            for apartment in all_apartments:
                if apartment.country == country:
                    cities.add(apartment.city)

        return country_city_dict

    def get_owners_apartments(self, owner):
        return self._get_all().filter(owner=owner)

    def get_realtors_apartments(self, realtor):
        return self._get_all().filter(realtor=realtor)


apartment_manager = ApartmentManager()
search_manager = SearchManager(apartment_manager)


def list_all(request):
    page = request.GET.get('page')
    order = request.GET.get('order', False)
    
    if order:
        if order.lower() in ORDER_CHOICES:
            request.session['order'] = order.lower()
    if request.session.get('order', None) == None:
        request.session['order'] = ORDER_CHOICES[2]

    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_all(page, order=request.session['order'])})


def list_featured(request):
    page = request.GET.get('page')
    return render(request, 'apartments/list.html', {'apartments': apartment_manager.get_featured(page, order=request.session['order'])})


def search(request):
    page = request.GET.get('page')
    order = request.GET.get('order', False)
    
    if order:
        if order.lower() in ORDER_CHOICES:
            request.session['order'] = order.lower()
    if request.session.get('order', None) == None:
        request.session['order'] = ORDER_CHOICES[2]
    context = {
        'search_country_cites': apartment_manager.build_country_city_dict(),
        'search_types'        : Apartment.TYPE_CHOICES,
        'search_prices'       : PRICE_RANGE,
        'search_sizes'        : SIZE_RANGE,
        'search_rooms'        : ROOMS_RANGE,
        'search_results'      : False,
    }
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_object = search_form.save(commit=False)
            search_object.created = datetime.now()
            search_object.populate(request.POST)
            if not request.user.is_anonymous:
                search_object.owner = request.user
            search_object.save()
            return redirect('search_results', search_id=search_object.search_id)

    context['apartments'] = apartment_manager.get_featured(page, order=request.session['order'])
    return render(request, 'apartments/search.html', context)


def search_results(request, search_id):
    try:
        search_object = search_manager.get_by_id(search_id)
    except ObjectDoesNotExist:
        return redirect('search')

    page = request.GET.get('page')
    order = request.GET.get('order', False)
    if order:
        if order.lower() in ORDER_CHOICES:
            request.session['order'] = order.lower()
    if request.session.get('order', None) == None:
        request.session['order'] = ORDER_CHOICES[2]
    found_apartments = search_manager.get_results(search_object)
    paginated_found_apartments = apartment_manager.paginate(found_apartments.order_by(request.session['order']), page)
    context = {
        'search_country_cites': apartment_manager.build_country_city_dict(),
        'search_types'        : Apartment.TYPE_CHOICES,
        'search_prices'       : PRICE_RANGE,
        'search_sizes'        : SIZE_RANGE,
        'search_rooms'        : ROOMS_RANGE,
        'search_results'      : True,
        'apartments'          : paginated_found_apartments
    }

    if request.method == "POST":
        return search(request)

    return render(request, 'apartments/search.html', context)


@login_required
def search_delete(request, search_id):
    try:
        search_object = search_manager.get_by_id(search_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if search_object.owner != request.user:
        return HttpResponseForbidden()

    search_object.delete()
    return redirect('my_apartments')

def view(request, apartment_id):
    images = ApartmentImages.objects.all().filter(apartment_id=apartment_id)   
    apartment = apartment_manager.get_by_id(apartment_id) 
    context = {
        'apartment'  : apartment,
        'images'     : images,
    }

    if apartment.realtor:
        realtor = UserProfile.objects.get(user_id=apartment.realtor.pk)
        context['realtor'] = realtor

    return render(request, 'apartments/view.html', context)


@login_required
def add(request):
    image_form_set = modelformset_factory(ApartmentImages, form=ApartmentImageForm, extra=MAX_NUMBER_OF_IMAGES)

    if request.method == "POST":
        apartment_form = ApartmentForm(request.POST)
        image_formset = image_form_set(request.POST, request.FILES)
        if apartment_form.is_valid() and image_formset.is_valid():
            apartment_object = apartment_form.save(commit=False)
            apartment_object.add_date = datetime.now()
            apartment_object.owner = request.user
            apartment_object.populate(request.POST)
            apartment_object.save()

            for i, form in enumerate(image_formset.cleaned_data):
                if not form:
                    continue
                image = form['image']
                primary = request.POST.get('primary', None) == '{}'.format(i)
                apartment_image = ApartmentImages(apartment_id=apartment_object, image=image, primary=primary)
                apartment_image.save()

            messages.success(request, 'New property: {} added to your apartments!'.format(apartment_object))
            return redirect('my_apartments')


    apartment_form = ApartmentForm()
    image_formset = image_form_set(queryset=ApartmentImages.objects.none())
    return render(request, 'apartments/add.html', {'apartment_form': apartment_form, 'image_formset': image_formset, 'features': Apartment.VALID_FEATURES})


@login_required
def my(request):
    owner = request.user
    context = {
        'your_apartments': apartment_manager.get_owners_apartments(owner),
        'your_searches'  : search_manager.get_owners_searches(owner)[:10]

    }

    if owner.is_staff or owner.is_superuser:
        context['apartment_approvals'] = apartment_manager.get_unapproved()
        context['apartment_realtor'] = apartment_manager.get_realtors_apartments(owner)

    return render(request, 'apartments/my.html', context)

class CanEditApartment(UserPassesTestMixin):
    def test_func(self):
        try:
            apartment = apartment_manager.get_by_id(self.kwargs['apartment_id'])
            if apartment == None:
                raise PermissionDenied('Apartment is not for you.')
        except ObjectDoesNotExist:
            raise PermissionDenied('Apartment is not for you.')
        if apartment.owner != self.request.user or not self.request.user.is_staff:
            raise PermissionDenied('You have .')
        return True

@method_decorator(login_required, name='dispatch')
class EditApartment(LoginRequiredMixin, CanEditApartment, UpdateView):
    model = Apartment
    form_class = EditApartmentForm
    template_name = 'apartments/edit.html'
    success_url = reverse_lazy('my_apartments') 

    def get_object(self):
        return apartment_manager.get_by_id(self.kwargs['apartment_id'])

    def get_context_data(self, **kwargs):
        context = super(EditApartment, self).get_context_data(**kwargs)
        Apart_img = ApartmentImages.objects.all().filter(apartment_id_id=self.kwargs['apartment_id'])
        image_form_set = modelformset_factory(ApartmentImages, form=ApartmentImageForm, extra=(MAX_NUMBER_OF_IMAGES-Apart_img.count()))
        image_formset = image_form_set(queryset=Apart_img)
        context['features_options'] = Apartment.VALID_FEATURES
        context['images'] = image_formset
        return context

    def form_valid(self, form):
        image_form_set = modelformset_factory(ApartmentImages, form=ApartmentImageForm, extra=MAX_NUMBER_OF_IMAGES)
        image_formset = image_form_set(self.request.POST, self.request.FILES)

        obj = form.save(commit=False)
        obj.features = self.request.POST.getlist('features_new')

        if image_formset.is_valid():
            for i, form in enumerate(image_formset.cleaned_data):
                if not form:
                    continue
                image = form['image']
                if image != None and isinstance(image, InMemoryUploadedFile):
                    if form['id'] != None:
                        old_image = ApartmentImages.objects.get(id=old_id)
                        old_image.delete()
                    primary = self.request.POST.get('primary_new', None) == '{}'.format(i)
                    new_image = ApartmentImages(apartment_id=obj, image=image, primary=primary)
                    new_image.save()

                else:
                    if self.request.POST.get('primary_new') != None:
                        primary = self.request.POST.get('primary_new', None) == '{}'.format(i)
                        update_image = form['id']
                        if update_image.primary:
                            update_image.primary = False
                            update_image.save()
                        if primary:
                            update_image = form['id']
                            update_image.primary = True
                            update_image.save()
                    if self.request.POST.get('form-{}-image-clear'.format(i), None) == 'on':
                        del_image = form['id']
                        del_image.delete()

        obj.save()
        messages.success(self.request, 'Your property: {} successfully updated!'.format(obj))
        return redirect('/apartments/view/{}'.format(self.kwargs['apartment_id']))

@login_required
def delete_apartment(request, apartment_id):
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
        if apartment == None:
            raise PermissionDenied('Apartment is not for you.')
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if apartment.owner != request.user or not request.user.is_staff:
        return HttpResponseForbidden()

    apartment.delete()

    messages.success(request, 'Property: {} was removed!'.format(apartment))
    return redirect('my_apartments')

@login_required
def approve_apartment(request, apartment_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()

    apartment.approved = True
    apartment.approval_date = datetime.now()
    apartment.realtor = request.user
    apartment.save()
    messages.success(request, 'Property: {} aproved!'.format(apartment))
    return redirect(reverse('my_apartments')+"#apartment-approvals")


@login_required
def unapprove_apartment(request, apartment_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if apartment.realtor != request.user:
        return HttpResponseForbidden()

    apartment.approved = False
    apartment.featured = False
    apartment.realtor = None
    apartment.save()

    messages.success(request, 'Property: {} un-aproved!'.format(apartment))
    return redirect(reverse('my_apartments')+"#realtor-apartments")


@login_required
def feature_apartment(request, apartment_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if apartment.realtor != request.user:
        return HttpResponseForbidden()

    apartment.featured = True
    apartment.save()

    messages.success(request, 'Property: {} featured!'.format(apartment))
    return redirect(reverse('my_apartments')+"#realtor-apartments")


@login_required
def unfeature_apartment(request, apartment_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if apartment.realtor != request.user:
        return HttpResponseForbidden()

    apartment.featured = False
    apartment.save()

    messages.success(request, 'Property: {} un-featured!'.format(apartment))
    return redirect(reverse('my_apartments')+"#realtor-apartments")


@login_required
def approve_sale_apartment(request, apartment_id):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        apartment = apartment_manager.get_by_id(apartment_id)
    except ObjectDoesNotExist:
        return HttpResponseForbidden()
    if apartment.realtor != request.user:
        return HttpResponseForbidden()
    if not apartment.sold:
        return HttpResponseForbidden()

    buyer = apartment.buyer
    apartment.buyer = None
    apartment.owner = buyer
    apartment.realtor = None
    apartment.approved = False
    apartment.featured = False
    apartment.sold = False
    apartment.save()

    messages.success(request, 'Sale of {} aproved. Congrats to {}!'.format(apartment, buyer))
    return redirect(reverse('my_apartments')+"#realtor-apartments")


def transfer_ownership(request, apartment_id):
    if request.user.is_authenticated:
        apartment = apartment_manager.get_by_id(apartment_id)
        owner = apartment.owner
        buyer = request.user
        try:
            buyer_creditcard = UserCreditCard.objects.get(user=buyer)
            buyer_profile = UserProfile.objects.get(user=buyer)
            seller_profile = UserProfile.objects.get(user=owner)
            
            # Check if the owner is not the same as the buyer then redirect back to search
            if buyer == owner:
                messages.error(request, 'You are trying to buy your own apartment, that does not work.')
                return redirect('/apartments/view/{}'.format(apartment_id))
            #elif len(str(buyer_creditcard.credit_card_number)) < 12:
            #    messages.error(request, 'Length of the creditcard number is incorrect')
            #    return redirect('payment_page')
            #elif  len(str(buyer_creditcard.credit_card_security_number)) < 3:
            #    messages.error(request, 'Security card number is incorrect')
            #    return redirect('payment_page')
            # Validate that the creditcard expiry is correct
            elif buyer_creditcard.credit_card_expiry >= datetime.now().date():
                if request.method == "POST":
                    apartment.owner = buyer
                    apartment.sold = True
                    apartment.sold_date = datetime.now().date()
                    apartment.previous_owner = owner
                    apartment.save()
                    messages.success(request, 'You just bought your self a house')
                    return redirect('my_apartments')
                template_name = 'payment/owner_transfer.html'
                return render(request, template_name, {'apartment': apartment, 'buyer': buyer_profile, 'seller': seller_profile})
            else:
                messages.error(request, 'The date on the credit card is invalid or expired.')
                return redirect('payment_page')
        except ObjectDoesNotExist:
            messages.error(request, 'No valid credit card found')
            return redirect('payment_page')
    else:
        messages.error(request, 'You have to be a <a href="/users/signup/">registered user</a> to and <a href="/users/login/">logged in</a> in order to purchase a property.')
        return redirect('/apartments/view/{}'.format(apartment_id))
