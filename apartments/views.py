from django.shortcuts import render


def list(request):
    return render(request, 'apartments/list.html')


def search(request):
    return render(request, 'apartments/search.html')


def view(request):
    return render(request, 'apartments/view.html')

