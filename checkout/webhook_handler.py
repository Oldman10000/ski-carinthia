from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django import template

from .models import Order, OrderLineItem
from resorts.models import Resort
from profiles.models import UserProfile

import json
import time
from decimal import Decimal


class StripeWH_Handler:
    """
    Handle stripe webhooks
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        sends the user a the confirmation email with pass
        """
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        plaintext = template.loader.get_template(
            'checkout/confirmation_emails/confirmation_email_body.txt')
        htmltemp = template.loader.get_template(
            'checkout/confirmation_emails/confirmation_email_body.html')
        c = {
            'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        }
        text_content = plaintext.render(c)
        html_content = htmltemp.render(c)

        msg = EmailMultiAlternatives(
            subject, text_content, settings.DEFAULT_FROM_EMAIL, [cust_email])
        msg.attach_alternative(html_content, "text/html")

        print(msg)

        msg.send()

    def handle_event(self, event):
        """
        handle a generic/unknown/unexpected http response
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        TWOPLACES = Decimal(10) ** -2
        grand_total = Decimal(
            round(intent.charges.data[0].amount / 100, 2)).quantize(TWOPLACES)

        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = billing_details.phone
                profile.default_street_address1 = billing_details.address.line1
                profile.default_street_address2 = billing_details.address.line2
                profile.default_postcode = billing_details.address.postal_code
                profile.default_town_or_city = billing_details.address.city
                profile.default_county = billing_details.address.state
                profile.default_country = billing_details.address.country
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    user_profile=profile,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    street_address1__iexact=billing_details.address.line1,
                    street_address2__iexact=billing_details.address.line2,
                    postcode__iexact=billing_details.address.postal_code,
                    town_or_city__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    country__iexact=billing_details.address.country,
                    order_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                print('exists')
                break
            except Order.DoesNotExist:
                print('doesnotexist')
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                    content=f'Webhook received: {event["type"]} |\
                         Success: Verified order already in database',
                    status=200)
        else:
            try:
                order = Order.objects.create(
                        full_name=billing_details.name,
                        email=billing_details.email,
                        phone_number=billing_details.phone,
                        street_address1=billing_details.address.line1,
                        street_address2=billing_details.address.line2,
                        postcode=billing_details.address.postal_code,
                        town_or_city=billing_details.address.city,
                        county=billing_details.address.state,
                        country=billing_details.address.country,
                        order_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                for item_id, adult_quantity in json.loads(bag).items():
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

                for item_id, child_quantity in json.loads(bag).items():
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

                for item_id, family_quantity in json.loads(bag).items():
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
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e} ',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} |\
                 SUCCESS: Created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
