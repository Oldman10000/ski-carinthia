from django.shortcuts import get_object_or_404
from resorts.models import Resort


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, adult_quantity in bag.items():
        if adult_quantity.get('adult_quantity'):
            product = get_object_or_404(Resort, pk=item_id)
            total += adult_quantity.get('adult_quantity') * product.adult_price
            product_count += adult_quantity.get('adult_quantity')
            bag_items.append({
                'item_id': item_id,
                'quantity': adult_quantity.get('adult_quantity'),
                'product': product,
                'adult_ticket': True,
            })

    for item_id, child_quantity in bag.items():
        if child_quantity.get('child_quantity'):
            product = get_object_or_404(Resort, pk=item_id)
            total += child_quantity.get('child_quantity') * product.child_price
            product_count += child_quantity.get('child_quantity')
            bag_items.append({
                'item_id': item_id,
                'quantity': child_quantity.get('child_quantity'),
                'product': product,
                'child_ticket': True,
            })

    for item_id, family_quantity in bag.items():
        if family_quantity.get('family_quantity'):
            product = get_object_or_404(Resort, pk=item_id)
            total += family_quantity.get(
                'family_quantity') * product.family_price
            product_count += family_quantity.get('family_quantity')
            bag_items.append({
                'item_id': item_id,
                'quantity': family_quantity.get('family_quantity'),
                'product': product,
                'family_ticket': True,
            })

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }

    return context
