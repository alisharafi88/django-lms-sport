from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from .carts import Cart
from apps.courses.models import Course, Package


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


def add_to_cart_view(request, product_id, product_type):
    """
    Add a product (either Course or Package) to the cart.
    """
    cart = Cart(request)

    if product_type == '1':
        product = get_object_or_404(Course, id=product_id)
    elif product_type == '2':
        product = get_object_or_404(Package, id=product_id)
    else:
        messages.error(request, _('Invalid product type!'))
        return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))

    cart.add(product)
    messages.success(request, _('Your product has been added to the cart successfully!'))

    return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))


def remove_from_cart_view(request, product_id, product_type):
    """
    Remove a product (either Course or Package) from the cart.
    """
    cart = Cart(request)

    if product_type == 'course':
        product = get_object_or_404(Course, id=product_id)
    elif product_type == 'package':
        product = get_object_or_404(Package, id=product_id)
    else:
        messages.error(request, _('Invalid product type!'))
        return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))

    cart.remove(product)
    messages.success(request, _('Your product has been removed from the cart successfully!'))

    return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))


def clear_cart_view(request):
    """
    Clear the entire cart.
    """
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, _('Your cart has been cleared successfully!'))

    return redirect(request.META.get('HTTP_REFERRER', 'courses:course_list'))
