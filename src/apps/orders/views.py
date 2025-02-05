import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import View
from django.db import transaction

from .models import Order, OrderItem, DVDOrderDetail
from .forms import CheckoutForm

from apps.carts.carts import Cart


logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class OrderCreateView(View):
    form_class = CheckoutForm
    template_name = 'orders/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, _('You cannot proceed to the checkout page because your cart is empty.'),
                             'warning', )
            logger.info('User  %s attempted to checkout with an empty cart.', request.user.username)
            return redirect('courses:course_list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        cart = Cart(request)
        logger.debug('Rendering checkout page for user %s with cart items: %s', request.user.username, cart)
        return render(request, self.template_name, {'cart': cart, 'form': self.form_class()})

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST)
        total_price, total_discounted_price = cart.get_total_price()
        logger.debug('User  %s is attempting to create an order with total price: %s and discounted price: %s',
                     request.user.username, total_price, total_discounted_price)

        if form.is_valid():
            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        customer=request.user,
                        total_price=total_discounted_price,
                    )
                    logger.info('Order created for user %s with order ID: %s', request.user.username, order.id)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            course=item['course_obj'],
                            unit_price=item['item_total_price'],
                        )
                        logger.debug('OrderItem created for order ID %s: %s', order.id, item)

                    if form.cleaned_data['is_active'] == Order.AccessStatus.DVD:
                        order.access_status = Order.AccessStatus.DVD
                        order.save()
                        DVDOrderDetail.objects.create(
                            order=order,
                            address=form.cleaned_data['shipping_address'],
                            city=form.cleaned_data['shipping_city'],
                            postal_code=form.cleaned_data['postal_code'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            phone_number=form.cleaned_data['phone_number'],
                            email=form.cleaned_data['email'],
                            order_note=form.cleaned_data['order_note']
                        )
                        logger.info('DVDOrderDetail created for order ID %s', order.id)

                    cart.clear()
                    logger.info('Cart cleared for user %s after order completion.', request.user.username)
                    messages.success(request, _('Your order was successfully completed!'), 'success')
                    return redirect('carts:cart')
            except Exception as e:
                logger.error('Error creating order for user %s: %s', request.user.username, e, exc_info=True)
                messages.error(request, _('Something went wrong. Please try again.'), 'error')
                return redirect('carts:cart')
        else:
            logger.warning('Form validation failed for user %s with errors: %s', request.user.username, form.errors)
            messages.error(request, _('Please correct the errors below:'), 'error')
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {errors[0]}', 'error')
            return redirect('carts:cart')
