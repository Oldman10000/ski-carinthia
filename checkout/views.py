from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from resorts.models import Resort
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            for item_id, adult_quantity in bag.items():
                if adult_quantity.get('adult_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort,
                        ticket_price=resort.adult_price,
                        quantity=adult_quantity.get('adult_quantity'),
                        ticket_type='Adult Pass',
                    )
                    order_line_item.save()

            for item_id, child_quantity in bag.items():
                if child_quantity.get('child_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort,
                        ticket_price=resort.child_price,
                        quantity=child_quantity.get('child_quantity'),
                        ticket_type='Child Pass',
                    )
                    order_line_item.save()

            for item_id, family_quantity in bag.items():
                if family_quantity.get('family_quantity'):
                    resort = Resort.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        resort=resort,
                        ticket_price=resort.family_price,
                        quantity=adult_quantity.get('family_quantity'),
                        ticket_type='Family Pass',
                    )
                    order_line_item.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            if request.user.is_authenticated:
                messages.error(request, "Your bag is empty")
                return redirect(reverse('resorts'))
            else:
                messages.error(
                    request, "You must be logged in to access checkout")
                return redirect(reverse('home'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'country': profile.default_country,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_email': order.email,
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    user = str(request.user)
    owner = str(order.user_profile)

    if user == owner:
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
