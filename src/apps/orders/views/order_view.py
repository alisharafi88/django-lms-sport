from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views import View
from django.db import transaction

import logging

from apps.courses.models import CourseMembership
from apps.orders.models import Order, OrderItem, DVDOrderDetail
from apps.orders.forms import CheckoutForm
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
        total_price, total_discounted_price = cart.get_total_price()

        logger.debug('Rendering checkout page for user %s with cart items: %s', request.user.username, cart)
        return render(
            request,
            self.template_name,
            {
                'cart': cart,
                'total_price': total_price,
                'total_discounted_price': total_discounted_price,
                'form': self.form_class()
            }
        )

    def post(self, request):
        cart = Cart(request)
        form = self.form_class(request.POST)
        total_price, total_discounted_price = cart.get_total_price()
        logger.debug('User  %s is attempting to create an order with total price: %s and discounted price: %s',
                     request.user.username, total_price, total_discounted_price)

        if form.is_valid():
            try:
                with transaction.atomic():
                    valid_items = []
                    enrolled_items = []
                    seen_products = set()

                    for item in cart:
                        product = item['product_obj']
                        content_type = ContentType.objects.get_for_model(product)
                        product_key = (content_type.id, product.id)

                        membership_exists = CourseMembership.objects.filter(
                            user=request.user,
                            content_type=content_type,
                            object_id=product.id
                        ).exists()

                        if membership_exists:
                            enrolled_items.append(product)
                        elif product_key not in seen_products:
                            seen_products.add(product_key)
                            valid_items.append(item)

                    if enrolled_items:
                        for product in enrolled_items:
                            messages.warning(
                                request,
                                _(f"You're already enrolled in {product.title}. Removed from order."),
                                'warning'
                            )
                        if not valid_items:
                            return redirect('courses:course_list')

                    order = Order.objects.create(
                        customer=request.user,
                        total_price=total_discounted_price,
                    )
                    logger.info('Order created for user %s with order ID: %s', request.user.username, order.id)

                    for item in valid_items:
                        product = item['product_obj']
                        content_type = ContentType.objects.get_for_model(product)

                        OrderItem.objects.get_or_create(
                            order=order,
                            content_type=content_type,
                            object_id=product.id,
                            defaults={'unit_price': item['item_total_price']}
                        )
                        logger.debug('Processing cart item: %s', item)
                        logger.debug('Product object: %s', product)
                        logger.debug('OrderItem created for order ID %s: %s', order.id, item)

                    if form.cleaned_data['status'] == Order.AccessStatus.DVD:
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

                    request.session['order_id'] = order.id
                    return redirect('orders:zp_payment_process')
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


def apply_coupon_view(request):
    if request.method == 'POST':
        logger.debug('Apply coupon view called')
        coupon_code = request.POST.get('coupon_code')
        logger.debug(f'Coupon code received: {coupon_code}')
        cart = Cart(request)
        try:
            cart.apply_coupon(coupon_code)
            total_price, final_price = cart.get_total_price()
            logger.debug(f'Total price: {total_price}, Final price: {final_price}')
            return JsonResponse({
                'success': True,
                'message': _('Coupon applied successfully.'),
                'coupon_code': coupon_code,
                'coupon_discount': cart.coupon_discount,
                'total_price': total_price,
                'final_price': final_price,
            })
        except ValueError as e:
            logger.error(f'Error applying coupon: {e}')
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


def remove_coupon_view(request):
    logger.debug('Remove coupon view called')
    if request.method == 'POST':
        cart = Cart(request)
        cart.remove_coupon()
        total_price, final_price = cart.get_total_price()
        logger.debug(f'Total price after removing coupon: {total_price}, Final price: {final_price}')
        return JsonResponse({
            'success': True,
            'message': _('Coupon removed successfully.'),
            'total_price': total_price,
            'final_price': final_price,
        })
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
