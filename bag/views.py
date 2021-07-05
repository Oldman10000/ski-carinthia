from django.shortcuts import render, redirect, reverse, HttpResponse


def view_bag(request):
    """
    returns bag page
    """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
    add items to bag
    """

    adult_quantity = int(request.POST.get('adult_quantity'))
    child_quantity = int(request.POST.get('child_quantity'))
    family_quantity = int(request.POST.get('family_quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    def add_quantity(quantity, type, item_id, bag):
        """
        adds quantity of specific pass type to bag
        """

        if quantity:
            if item_id in list(bag.keys()):
                if f'{type}' in bag[item_id]:
                    bag[item_id][f'{type}'] += quantity
                else:
                    bag[item_id][f'{type}'] = quantity
            else:
                bag[item_id] = {f'{type}': quantity}

    add_quantity(adult_quantity, 'adult_quantity', item_id, bag)
    add_quantity(child_quantity, 'child_quantity', item_id, bag)
    add_quantity(family_quantity, 'family_quantity', item_id, bag)

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

    def add_quantity(quantity, type, item_id, bag):
        """
        adds quantity of specific pass type to bag
        """

        if quantity:
            if item_id in list(bag.keys()):
                if f'{type}' in bag:
                    bag[item_id][f'{type}'] += quantity
                else:
                    bag[item_id][f'{type}'] = quantity
            else:
                bag[item_id] = {f'{type}': quantity}

    bag = request.session.get('bag', {})
    if adult_quantity is not None:
        if adult_quantity > 0:
            add_quantity(adult_quantity, 'adult_quantity', item_id, bag)
        else:
            del bag[item_id]['adult_quantity']
            if not bag[item_id]:
                bag.pop(item_id)
    if child_quantity is not None:
        if child_quantity > 0:
            add_quantity(child_quantity, 'child_quantity', item_id, bag)
        else:
            del bag[item_id]['child_quantity']
            if not bag[item_id]:
                bag.pop(item_id)
    if family_quantity is not None:
        if family_quantity > 0:
            add_quantity(family_quantity, 'family_quantity', item_id, bag)
        else:
            del bag[item_id]['family_quantity']
            if not bag[item_id]:
                bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    removes item from the shopping bag
    """

    try:
        bag = request.session.get('bag', {})
        type = request.POST['type']

        del bag[item_id][f'{type}']
        if not bag[item_id]:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
