from django.shortcuts import render


def index(request):
    """
    returns index page
    """
    return render(request, 'home/index.html')
