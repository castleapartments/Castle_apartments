from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from base.models import UserProfile, UserCreditCard
from base.forms import UserForm, ProfileForm, CreditCardForm



# Create your views here.

def index(request):
    return render(request, "index.html")

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
                messages.error(request,'This account has been deactivated!')
                return render(request, "login.html")
        else:

            messages.error(request,'Username or password not correct!')
            return render(request, "login.html")
            
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
                new_user = authenticate(username=user.username,
                                    password=user.password,)
                login(request, new_user)
                messages.success(request,'Welcome to the castle {}!'.format(user.username))
            return redirect('index')
        else:
            messages.error(request,'There is something wrong with your sign up mate!')
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
class ProfileUpdateView(TestUserCanViewUser, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'base/profile_edit.html'
    success_message = "Profile updated successfully!"
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
class CreateCreditCardView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserCreditCard
    form_class = CreditCardForm
    template_name = 'payment/creditcard_create.html'
    success_message = "Credit Card saved successfully!"
    success_url = reverse_lazy('payment_page')
    
    def form_valid(self, form):
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
class UpdateCreditCardView(LoginRequiredMixin, TestUserCanViewUser,SuccessMessageMixin, UpdateView):
    model = UserCreditCard
    form_class = CreditCardForm
    template_name = 'payment/creditcard_create.html'
    success_message = "Credit Card updated successfully!"
    success_url = reverse_lazy('payment_page')   

    def get_object(self):
        return UserCreditCard.objects.get(user_id=self.kwargs['pk'])
