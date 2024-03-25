from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')


def random_number(request):
    return render(request, 'pages/random_number.html')
