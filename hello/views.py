from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy


from hello.models import Person, Card
from hello.forms import PersonForm, CardForm


from .models import Greeting





# Create your views here.

def index(request):
    # return HttpResponse('Hello from Python!')
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
    template_name = 'hello/card_update_form.html'
    success_url = reverse_lazy('card_list')    

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'hello/person_update_form.html'
    success_url = reverse_lazy('person_list')    

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")    