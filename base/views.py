from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from django.contrib.auth import authenticate, login, logout
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from base.models import Person, Card, UserProfile
from base.forms import UserForm, PersonForm, CardForm, ProfileForm



# Create your views here.

def index(request):
    return render(request, "index.html")

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

def forget_password(request):
    return redirect('/users/password_reset/')

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
            user.save()

            # After the user is created the profile must be created
            # Start by searching the user to get the User instance
            find_user = User.objects.get(username=username)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            
            messages.info(request,'Welcome!')
            return redirect('index')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, "signup.html")

class profileupdate(UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')  

@login_required
def profile1(request):
    if request.method == "POST":
        profile_form = ProfileForm(data=request.POST)
    return render(request, "profile.html", { 'form': profile_form })

@login_required
def profile(request):
    if request.method == "POST":
        profile_form = ProfileForm(data=request.POST)

        if profile_form.is_valid():
            
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Needs some box to notify that it was succesfully saved
            messages.info(request,'Profile Saved!')
            #return redirect('index')
            return redirect('/profile/{}'.format(profile.id))
            return HttpResponse(profile.user.username)
        else:
            
            return HttpResponse(profile_form.errors)
    else:
        profile_form = ProfileForm()
    return render(request, "profile_edit.html", { 'form': profile_form })


#@login_required
#def profile(request):
#    if request.method == "POST":
#        profile_form = ProfileForm(data=request.POST)
#
#        if profile_form.is_valid():
#            
#            profile = profile_form.save(commit=False)
#            profile.user = request.user
#            profile.save()
#            
#            # Needs some box to notify that it was succesfully saved
#            messages.info(request,'Profile Saved!')
#            return redirect('index')
#        else:
#            return HttpResponse(profile_form.errors)
#    else:
#        profile_form = ProfileForm()
#    return render(request, "profile.html", { 'form': profile_form })
 

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    def get_queryset(self):
        try:
            return UserProfile.objects.filter(user_id=self.request.user.id)
        except UserProfile.DoesNotExist:
            return redirect('/profile')

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


def test(request):
    current_user = request.user
    return HttpResponse(current_user.username)