from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .models import Order, OrderItem

from carts.carts import Cart



def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'), 'warnning',)
        return  redirect('courses:course_list')

    total_price, total_discounted_price = cart.get_total_price()

    order = Order.objects.create(
        customer=request.user,
        total_price=total_discounted_price, 
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            course=item['course_obj'],
            unit_price=item['item_total_price'], 
        )

    cart.clear()

    return redirect('carts:cart')
