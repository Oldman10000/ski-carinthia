from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages
from resorts.models import Resort


def view_bag(request):
    """
    returns bag page
    """
    bag = request.session.get('bag', {})
    print(bag)
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    add items to bag
    """

    resort = get_object_or_404(Resort, pk=item_id)
    adult_quantity = int(request.POST.get('adult_quantity'))
    child_quantity = int(request.POST.get('child_quantity'))
    family_quantity = int(request.POST.get('family_quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    def add_quantity(
            quantity, ticket_type, item_id, bag, resort, friendly_ticket):
        """
        adds quantity of specific pass ticket_type to bag
        """
        if quantity:
            if item_id in list(bag.keys()):
                if f'{ticket_type}' in bag[item_id]:
                    bag[item_id][f'{ticket_type}'] += quantity
                    messages.success(
                        request, f'Added {quantity} {resort}, {friendly_ticket}\
                             to your bag')
                else:
                    bag[item_id][f'{ticket_type}'] = quantity
                    messages.success(
                        request, f'Added {quantity} {resort}, {friendly_ticket}\
                             to your bag')
            else:
                bag[item_id] = {f'{ticket_type}': quantity}
                messages.success(
                    request, f'Added {quantity} {resort}, {friendly_ticket}\
                         to your bag')

    add_quantity(
        adult_quantity,
        'adult_quantity',
        item_id,
        bag,
        resort.name,
        'adult pass')
    add_quantity(
        child_quantity,
        'child_quantity',
        item_id,
        bag,
        resort.name,
        'child pass')
    add_quantity(
        family_quantity,
        'family_quantity',
        item_id,
        bag,
        resort.name,
        'child pass')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    adjusts bag by specified amount
    """

    if request.POST.get('adult_quantity'):
        adult_quantity = int(request.POST.get('adult_quantity'))
        child_quantity = None
        family_quantity = None
    elif request.POST.get('child_quantity'):
        child_quantity = int(request.POST.get('child_quantity'))
        adult_quantity = None
        family_quantity = None
    elif request.POST.get('family_quantity'):
        family_quantity = int(request.POST.get('family_quantity'))
        adult_quantity = None
        child_quantity = None
    else:
        return redirect(reverse('view_bag'))

    resort = get_object_or_404(Resort, pk=item_id)
    bag = request.session.get('bag', {})

    if adult_quantity is not None:
        if adult_quantity > 0:
            bag[item_id]['adult_quantity'] = adult_quantity
            messages.success(
                request, f'Updated {resort}, adult passes to {adult_quantity}')
        else:
            del bag[item_id]['adult_quantity']
            if not bag[item_id]:
                bag.pop(item_id)
            messages.success(
                request, f'Removed {resort}, adult passes from your bag')

    if child_quantity is not None:
        if child_quantity > 0:
            bag[item_id]['child_quantity'] = child_quantity
            messages.success(
                request, f'Updated {resort}, child passes to {child_quantity}')
        else:
            del bag[item_id]['child_quantity']
            if not bag[item_id]:
                bag.pop(item_id)
            messages.success(
                request, f'Removed {resort}, child passes from your bag')

    if family_quantity is not None:
        if family_quantity > 0:
            bag[item_id]['family_quantity'] = family_quantity
            messages.success(
                request, f'Updated {resort}, family passes to \
                {family_quantity}')
        else:
            del bag[item_id]['family_quantity']
            if not bag[item_id]:
                bag.pop(item_id)
            messages.success(
                request, f'Removed {resort}, family passes from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    removes item from the shopping bag
    """

    resort = get_object_or_404(Resort, pk=item_id)

    try:
        bag = request.session.get('bag', {})
        ticket_type = request.POST['type']
        friendly_type = ticket_type.replace('_quantity', '')

        del bag[item_id][f'{ticket_type}']
        if not bag[item_id]:
            bag.pop(item_id)
        messages.success(
                request, f'Removed {resort}, {friendly_type}\
                     passes from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
