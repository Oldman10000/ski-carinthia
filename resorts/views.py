from django.shortcuts import render
from .models import Resort


def all_resorts(request):
    """
    returns all resorts page
    """

    resorts = Resort.objects.all()

    context = {
        'resorts': resorts,
    }

    return render(request, 'resorts/resorts.html', context)
