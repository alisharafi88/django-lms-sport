from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.carts.carts import Cart
from apps.courses.models import Package, CourseMembership, CourseTelegramLink, Course
from apps.orders.models import Order


def enrollment_process(request, order, data=None):
    with transaction.atomic():
        update_order_payment_status(request, order, data)
        enroll_student_in_courses(request, order)
        clear_cart(request)
        messages.success(request, _('Payment successful! You are now enrolled in your courses.'))


def update_order_payment_status(request, order, data):
    if data is not None:
        order.zarinpal_ref_id = data['ref_id']
        order.zarinpal_data = data
    if 'coupon_code' in request.session:
        order.coupon_code = request.session['coupon_code']

    order.status = Order.OrderStatus.PAID
    order.save()


def enroll_student_in_courses(request, order):
    user = order.customer
    for item in order.items.all():
        product = item.product
        if isinstance(product, Package):
            enroll_in_package(request, user, product)
        elif isinstance(product, Course):
            enroll_in_course(request, user, product)


def enroll_in_package(request, user, package):
    CourseMembership.objects.get_or_create(
        user=user,
        content_type=ContentType.objects.get_for_model(Package),
        object_id=package.id
    )
    for course in package.courses.all():
        enroll_in_course(request, user, course)


def enroll_in_course(request, user, course):
    CourseMembership.objects.get_or_create(
        user=user,
        content_type=ContentType.objects.get_for_model(Course),
        object_id=course.id
    )
    assign_telegram_link(request, user, course)


def clear_cart(request):
    cart = Cart(request)
    cart.finalize_purchase()


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
