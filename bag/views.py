from django.shortcuts import render


def view_bag(request):
    """
    returns bag page
    """

    return render(request, 'bag/bag.html')
