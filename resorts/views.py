from django.shortcuts import render, get_object_or_404
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


def resort_detail(request, resort_id):
    """
    returns resort detail page
    """

    resort = get_object_or_404(Resort, pk=resort_id)

    context = {
        'resort': resort,
    }

    return render(request, 'resorts/resort_detail.html', context)
