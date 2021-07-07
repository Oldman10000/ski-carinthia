from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51J2Ev6LhlFiglby6HfLFyWlWEMMe3b2HGBVSHrPtkom6i2Ov8TGLuF1BDdRVGgshzGtweDVUc2SczfW4OQ5VXx4I00bk9G0Bam',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
