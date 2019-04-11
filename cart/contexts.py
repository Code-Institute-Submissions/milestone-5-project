from django.shortcuts import get_object_or_404
from issue_tracker.models import Issue


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page
    """

    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0
    for id, quantity in cart.items():
        product = get_object_or_404(Issue, pk=id)
        price = product.hourly_rate * product.hours_required
        total += quantity * price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product, 'price': price})

    return {'cart_items': cart_items, 'total': total,
            'product_count': product_count}
