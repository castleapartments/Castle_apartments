from django.shortcuts import render
from .forms import ApartmentForm


def list(request):
    return render(request, 'apartments/list.html')


def search(request):
    return render(request, 'apartments/search.html')


def view(request):
    return render(request, 'apartments/view.html')


def add(request):
    if request.method == "POST":
        form = ApartmentForm(request.POST)
        if form.is_valid():
            form.save()

    form = ApartmentForm()
    return render(request, 'apartments/add.html', {'form': form})
