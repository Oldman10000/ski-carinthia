from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from resorts.models import Resort
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()

            for item_id, adult_quantity in bag.items():
                if adult_quantity.get('adult_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort + 'adult pass',
                        ticket_price=resort.adult_price,
                        quantity=adult_quantity.get('adult_quantity'),
                    )
                    order_line_item.save()

            for item_id, child_quantity in bag.items():
                if child_quantity.get('child_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort + 'child pass',
                        ticket_price=resort.child_price,
                        quantity=child_quantity.get('child_quantity'),
                    )
                    order_line_item.save()

            for item_id, family_quantity in bag.items():
                if family_quantity.get('family_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort + 'family pass',
                        ticket_price=resort.family_price,
                        quantity=adult_quantity.get('family_quantity'),
                    )
                    order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. Your pass(es) will be \
            emailed to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
