from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .carts import Cart
from apps.courses.models import Course, Package
from apps.utils.numbers.convert_numbers import PersianNumberConverter


def cart_view(request):
    """
    Display the cart page with cart items and total prices.
    """
    cart = Cart(request)
    total_price, total_discounted_price = cart.get_total_price()

    cart_items = list(cart)

    return render(request, 'carts/cart.html', {
        'carts': cart_items,
        'total_price': total_price,
        'total_discounted_price': total_discounted_price
    })


@require_POST
def add_to_cart_view(request, product_id, product_type):
    cart = Cart(request)
    product = _get_product(product_type, product_id)
    if not product:
        return JsonResponse({'status': 'error', 'message': _('Invalid product type!')}, status=400)

    cart.add(product)
    response_data = {
        'status': 'success',
        'message': _('Product added to cart!'),
        'cart_count': PersianNumberConverter.to_persian(cart.get_total_price(), humanize=True),
        'product_id': product_id,
        'product_type': product_type,
    }
    return JsonResponse(response_data)


@require_POST
def remove_from_cart_view(request, product_id, product_type):
    cart = Cart(request)
    product = _get_product(product_type, product_id)
    if not product:
        return JsonResponse({'status': 'error', 'message': _('Invalid product type!')}, status=400)

    cart.remove(product)

    is_empty = False if len(cart) > 0 else True
    total_price, total_discounted_price = None, None
    if not is_empty:
        total_price, total_discounted_price = cart.get_total_price()

    response_data = {
        'status': 'success',
        'message': _('Product removed from cart!'),
        'total_price': PersianNumberConverter.to_persian(total_price, humanize=True),
        'total_discounted_price': PersianNumberConverter.to_persian(total_discounted_price, humanize=True),
        'product_id': product_id,
        'product_type': product_type,
        'cart_empty': is_empty,
    }
    return JsonResponse(response_data)


def _get_product(product_type, product_id):
    if product_type == '1' or product_type == 'course':
        return get_object_or_404(Course, id=product_id)
    elif product_type == '2' or product_type == 'package':
        return get_object_or_404(Package, id=product_id)
    return None


@require_POST
def clear_cart_view(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        return JsonResponse({
            'status': 'success',
            'message': _('Cart cleared'),
            'cart_count': 0,
            'cart_total': 0,
            'cart_empty': True,
        })
    return JsonResponse({'status': 'success', 'message': _('Cart already empty')})
