from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Resort
from django.core.paginator import Paginator


def all_resorts(request):
    """
    returns all resorts page
    """

    resorts = Resort.objects.all()
    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'price':
                sortkey = 'adult_price'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            resorts = resorts.order_by(sortkey)

        if 'family_friendly' in request.GET:
            resorts = resorts.filter(family_friendly=True)

        if 'scenic' in request.GET:
            resorts = resorts.filter(scenic=True)

        if 'large' in request.GET:
            resorts = resorts.filter(size='large')
        
        if 'medium' in request.GET:
            resorts = resorts.filter(size='medium')
        
        if 'small' in request.GET:
            resorts = resorts.filter(size='small')

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('resorts'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            resorts = resorts.filter(queries)

    paginator = Paginator(resorts, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_sorting = f'{sort}_{direction}'

    context = {
        'resorts': resorts,
        'page_obj': page_obj,
        'search_term': query,
        'current_sorting': current_sorting,
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
