from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from base.models import Person, Card, UserProfile, UserCreditCard
from base.forms import UserForm, PersonForm, CardForm, ProfileForm, CreditCardForm



# Create your views here.

def index(request):
    return render(request, "index.html")

# ********************************
# <--TEST - REMOVE IN CLEAN UP -->

class PersonListView(ListView):
    model = Person
    context_object_name = 'people'

class CardListView(ListView):
    model = Card
    context_object_name = 'cards'

class PersonCreateView(CreateView):
    model = Person
    fields = ('name', 'email', 'job_title', 'bio')
    success_url = reverse_lazy('person_list')

class CardCreateView(CreateView):
    model = Card
    fields = ('name',)
    success_url = reverse_lazy('card_list')    

def singlecard(request):
    return render(request, 'base/singlecard.html')

def apartmentlist(request):
    return render(request, 'base/apartment_list.html')

class CardUpdateView(UpdateView):
    model = Card
    form_class = CardForm
    template_name = 'base/card_update_form.html'
    success_url = reverse_lazy('card_list')    

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'base/person_update_form.html'
    success_url = reverse_lazy('person_list')    

class PersonAndCardListView(ListView):
    context_object_name = 'pc_list'    
    template_name = 'base/pc_list.html'
    queryset = Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PersonAndCardListView, self).get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        context['cards'] = Card.objects.all()
        # And so on for more models
        return context



# <-- /TEST - REMOVE IN CLEAN UP -->
# ********************************



def forget_password(request):
    return redirect('/users/password_reset/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error bellow')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:

            messages.error(request,'username or password not correct')
            return redirect('/login/')
    else:
        return render(request, "login.html")


#login is used internally
#def login(request):
#    return render(request, "login.html")

def signup(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            username = user.username
            if user:
                user.save()

                # After the user is created the profile must be created
                # Start by searching the user to get the User instance
                find_user = User.objects.get(username=username)
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.country = "US"
                profile.save()

                registered = True
                
                messages.info(request,'Welcome!')
            return redirect('index')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, "signup.html")

def profile(request):
    return redirect('/profile/{}'.format(request.user.id))    


class TestUserCanViewUser(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.id == self.kwargs['pk']:
            return True
        raise PermissionDenied('Only Admins can view all users.')


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(TestUserCanViewUser, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'base/profile_edit.html'
    success_url = reverse_lazy('profile') 

    def get_object(self):
        return UserProfile.objects.all().get(user_id=self.kwargs['pk'])


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(LoginRequiredMixin, TestUserCanViewUser, DetailView):
    model = UserProfile

    def get_object(self):
        
        # IF a superuser is created via cmd-line, the profile does not excist. 
        # This should rectify that.
        if self.request.user.is_superuser:
            if User.objects.filter(id = self.kwargs['pk']).exists():
                try:
                    userprofiletest = UserProfile.objects.get(user_id=self.kwargs['pk'])
                except UserProfile.DoesNotExist:
                    profile = UserProfile()
                    profile.user_id = self.request.user.id
                    profile.country = "US"
                    profile.sex ="Male"
                    profile.email = self.request.user.email
                    profile.ssn = 12345678
                    profile.save()

        return UserProfile.objects.get(user_id=self.kwargs['pk'])




class TestUserIsSuper(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        raise PermissionDenied('Only Admins can view all users.')



@method_decorator(login_required, name='dispatch')
class UserListView(LoginRequiredMixin, TestUserIsSuper, ListView):
    model = User
    context_object_name = 'users'    
    template_name = 'users/user_list.html'
    queryset = User.objects.all()
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['profiles'] = UserProfile.objects.all()
        # And so on for more models
        return context



def payment(request):
    if UserCreditCard.objects.filter(user_id = request.user.id).exists():
        return redirect('/payment/{}'.format(request.user.id))
    else:
        return redirect('/payment/add')

@method_decorator(login_required, name='dispatch')
class CreateCreditCardView(LoginRequiredMixin, CreateView):
    model = UserCreditCard
    form_class = CreditCardForm
    template_name = 'payment/creditcard_create.html'
    success_url = reverse_lazy('payment_page')
    
    def form_valid(self, form):
        print('test')
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('/payment/')

@method_decorator(login_required, name='dispatch')
class ViewCreditCardView(LoginRequiredMixin, TestUserCanViewUser, DetailView):
    model = UserCreditCard
    template_name = 'payment/creditcard_details.html'

    def get_object(self):        
        return UserCreditCard.objects.get(user_id=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class UpdateCreditCardView(LoginRequiredMixin, TestUserCanViewUser, UpdateView):
    model = UserCreditCard
    form_class = CreditCardForm
    template_name = 'payment/creditcard_create.html'
    success_url = reverse_lazy('payment_page')   

    def get_object(self):
        return UserCreditCard.objects.get(user_id=self.kwargs['pk'])

def test(request):
    current_user = request.user
    return HttpResponse(current_user.username)