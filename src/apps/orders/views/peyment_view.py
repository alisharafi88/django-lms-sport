from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from apps.orders.models import Order
from apps.orders.enrollment import enrollment_process
from apps.orders.zarinpal import send_request, verify, ZP_API_STARTPAY


def payment_process(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.total_price
    if toman_total_price == 0:
        enrollment_process(request, order)
        return redirect('accounts:student_dashboards')

    rial_total_price = toman_total_price * 10

    description = f'#{order.id}: {order.customer.first_name} {order.customer.last_name}'
    callback_url = request.build_absolute_uri(reverse('orders:zp_payment_callback'))
    user_phone = str(request.user.phone_number)

    res = send_request(
        amount=rial_total_price,
        description=description,
        phone=user_phone,
        callback_url=callback_url
    )
    if res['status']:
        data = res['data']
        authority = data['authority']
        order.zarinpal_authority = authority
        order.save()

        if 'errors' not in data or len(data['errors']) == 0:
            return redirect('{zp_api_startpay}{authority}'.format(zp_api_startpay=ZP_API_STARTPAY, authority=authority))
        else:
            return HttpResponse('An unexpected error occurred during payment verification')
    else:
        return HttpResponse(res['error'])


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.total_price
    rial_total_price = toman_total_price * 10
    if payment_status == 'OK':
        with transaction.atomic():
            response = verify(
                authority=payment_authority,
                amount=rial_total_price
            )
            if response.get('status'):
                if 'data' in response['res'] and (
                        'errors' not in response['res']['data'] or len(response['res']['data']['errors'] == 0)):
                    data = response['res']['data']
                    payment_code = data['code']

                    if payment_code == 100:
                        enrollment_process(request, order, data)
                        return redirect('accounts:student_dashboards')

                    if payment_status == 101:
                        messages.info(request, _('Payment was already verified'))
                        return redirect('accounts:student_dashboard')

                    request.session['dvd_shipping_price'] = 0
                    messages.error(
                        request,
                        _('Payment verification failed: %(message)s') % {
                            'message': data.get('message', _('Unknown error'))}
                    )
                    return redirect('carts:cart')

            return HttpResponse(response['error'])

    order.status = Order.OrderStatus.CANCELED
    order.save()
    request.session['dvd_shipping_price'] = 0
    messages.error(request, _('The payment has been canceled.'))
    return redirect('carts:cart')
