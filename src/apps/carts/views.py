from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from .carts import Cart
from apps.courses.models import Course


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


def add_to_cart_view(request, course_id):
    """
    Add a course to the cart.
    """
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.add(course)
    messages.success(request, _('Your course has been added to the cart successfully!'))

    return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))


def remove_course_view(request, course_id):
    """
    Remove a course from the cart.
    """
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    messages.success(request, _('Your course has been removed from the cart successfully!'))

    return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))


def clear_cart_view(request):
    """
    Clear the entire cart.
    """
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, _('Your cart has been cleared successfully!'))

    return redirect('courses:course_list')
