from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Resort


def all_resorts(request):
    """
    returns all resorts page
    """

    resorts = Resort.objects.all()
    query = None

    if request.GET:
        if 'family_friendly' in request.GET:
            resorts = resorts.filter(family_friendly=True)

        if 'scenic' in request.GET:
            resorts = resorts.filter(scenic=True)

        if 'large' in request.GET:
            resorts = resorts.filter(size='large')

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('resorts'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            resorts = resorts.filter(queries)

    context = {
        'resorts': resorts,
        'search_term': query,
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
