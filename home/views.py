from django.shortcuts import render
from django.core.serializers import serialize

from resorts.models import Resort


def index(request):
    """
    returns index page
    """

    context = {
        'resorts': serialize("json", Resort.objects.all(),)
    }

    return render(request, 'home/index.html', context)
