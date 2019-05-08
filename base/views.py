from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from base.models import Person, Card
from base.forms import PersonForm, CardForm


from .models import Greeting





# Create your views here.

def index(request):
    return render(request, "index.html")

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

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
            print("Someone tried to login and failed!")
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, "login.html")


#login is used internally
#def login(request):
#    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

