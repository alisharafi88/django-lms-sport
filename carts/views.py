from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from carts.carts import Cart
from courses.models import Course


def cart_view(request):
    cart = Cart(request)
    total_price, total_discounted_price = cart.get_total_price()
    return render(request, 'carts/cart.html', {
        'carts': cart,
        'total_price': total_price,
        'total_discounted_price': total_discounted_price
    })


def add_to_cart_view(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.add(course)
    messages.success(request, _('Your course added to cart successfully!'))
    return redirect(request.META.get('HTTP_REFERER', 'carts:cart'))


def remove_course_view(request, course_id):
    cart = Cart(request)
    course = get_object_or_404(Course, id=course_id)
    cart.remove(course)
    messages.success(request, _('Your course removed from cart successfully!'))
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart'))


def clear_cart_view(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, _('Your cart cleared successfully!'))
    return redirect('courses:course_list')
