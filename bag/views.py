from django.shortcuts import render, redirect


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

    if adult_quantity:
        if item_id in list(bag.keys()):
            if 'adult_quantity' in bag:
                bag[item_id]['adult_quantity'] += adult_quantity
            else:
                bag[item_id]['adult_quantity'] = adult_quantity
        else:
            bag[item_id] = {'adult_quantity': adult_quantity}

    if child_quantity:
        if item_id in list(bag.keys()):
            if 'child_quantity' in bag:
                bag[item_id]['child_quantity'] += child_quantity
            else:
                bag[item_id]['child_quantity'] = child_quantity
        else:
            bag[item_id] = {'child_quantity': child_quantity}

    if family_quantity:
        if item_id in list(bag.keys()):
            if 'family_quantity' in bag:
                bag[item_id]['family_quantity'] += family_quantity
            else:
                bag[item_id]['family_quantity'] = family_quantity
        else:
            bag[item_id] = {'family_quantity': family_quantity}

    request.session['bag'] = bag
    return redirect(redirect_url)
