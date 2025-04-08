from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.carts.carts import Cart
from apps.courses.models import CourseMembership, CourseTelegramLink, Package, Course
from apps.orders.models import Order
from apps.orders.zarinpal import send_request, verify, ZP_API_STARTPAY


def payment_process(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.total_price
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
                        # Update payment status
                        order.status = Order.OrderStatus.PAID
                        order.zarinpal_ref_id = data['ref_id']
                        order.zarinpal_data = data
                        order.save()
                        # Enroll student in courses
                        for item in order.items.all():
                            product = item.product
                            user = order.customer

                            if isinstance(product, Package):  # package
                                # package-level
                                CourseMembership.objects.get_or_create(
                                    user=user,
                                    content_type=ContentType.objects.get_for_model(Package),
                                    object_id=product.id
                                )
                                # course-level
                                courses = product.courses.all()
                                for course in courses:
                                    CourseMembership.objects.get_or_create(
                                        user=user,
                                        content_type=ContentType.objects.get_for_model(Course),
                                        object_id=course.id
                                    )
                                    assign_telegram_link(request, user, course)
                            elif isinstance(product, Course):  # course
                                CourseMembership.objects.get_or_create(
                                    user=user,
                                    content_type=ContentType.objects.get_for_model(Course),
                                    object_id=product.id
                                )
                                assign_telegram_link(request, user, product)

                        # Clear cart

                        cart = Cart(request)
                        cart.finalize_purchase()
                        messages.success(request, _('Payment successful! You are now enrolled in your courses.'))
                        return redirect('accounts:student_dashboards')
                    if payment_status == 101:
                        messages.info(request, _('Payment was already verified'))
                        return redirect('accounts:student_dashboard')

                    messages.error(
                        request,
                        _('Payment verification failed: %(message)s') % {
                            'message': data.get('message', _('Unknown error'))}
                    )
                    return redirect('carts:cart')

            return HttpResponse(response['error'])

    messages.error(request, _('An unexpected error occurred during payment verification'))
    return redirect('carts:cart')


def assign_telegram_link(request, user, course):
    link = CourseTelegramLink.objects.filter(
        course=course,
        is_used=False
    ).select_for_update().first()

    if link:
        link.user = user
        link.is_used = True
        link.date_used = timezone.now()
        link.save()
    else:
        messages.warning(request,
                         _('Some Telegram links couldn\'t be assigned. Please contact support or send ticket if you don\'t receive your invite links.'))

        # sms_admins(
        #     f"No Telegram links for course: {course.title}",
        #     f"User {user} needs a link for course ID {course.id}"
        # )
