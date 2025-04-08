from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from apps.courses.models import Course, Package, CourseMembership, Coupon, CouponUsage

COURSE_TYPE = 'course'
PACKAGE_TYPE = 'package'


class Cart:
    CART_SESSION_ID = 'cart'
    CART_COUPON_CODE_ID = 'coupon_code'
    CART_COUPON_DISCOUNT = 'coupon_discount'

    def __init__(self, request):
        """
        Initialize the cart for both courses and packages.
        """
        self.request = request
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            cart = self.session[self.CART_SESSION_ID] = []
        self.cart = cart
        self.products = None

        coupon_code = self.session.get(self.CART_COUPON_CODE_ID, None)
        if not coupon_code:
            coupon_code = None
        self.coupon_code = coupon_code

        coupon_discount = self.session.get(self.CART_COUPON_DISCOUNT, 0)
        if not coupon_discount:
            coupon_discount = 0
        self.coupon_discount = coupon_discount

        self.course_ct = ContentType.objects.get_for_model(Course)
        self.package_ct = ContentType.objects.get_for_model(Package)

    def add(self, product):
        """
        Add a product (either Course or Package) to the cart.
        """
        product_type = COURSE_TYPE if isinstance(product, Course) else PACKAGE_TYPE
        product_id = str(product.id)
        item = {'type': product_type, 'id': product_id}

        user = self.request.user
        if user.is_authenticated:
            content_type = self.course_ct if product_type == COURSE_TYPE else self.package_ct
            if CourseMembership.objects.filter(
                    user=user,
                    content_type=content_type,
                    object_id=product.id
            ).exists():
                messages.warning(self.request, "You're already enrolled in this product.")
                return

        if item not in self.cart:
            self.cart.append(item)
            self.save()

    def save(self):
        """Save the cart in the session."""
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product (either Course or Package) from the cart.
        """
        product_type = COURSE_TYPE if isinstance(product, Course) else PACKAGE_TYPE
        product_id = str(product.id)
        item = {'type': product_type, 'id': product_id}
        if item in self.cart:
            self.cart.remove(item)
            self.save()

    def load_products(self):
        """
        Load products while excluding enrolled items and notify the user.
        """
        if self.products is not None:
            return

        user = self.request.user
        items_removed = False

        if user.is_authenticated:
            memberships = CourseMembership.objects.filter(user=user).select_related('content_type')

            enrolled_course_ids = set()
            enrolled_package_ids = set()
            for membership in memberships:
                if membership.content_type.model == 'course':
                    enrolled_course_ids.add(membership.object_id)
                elif membership.content_type.model == 'package':
                    enrolled_package_ids.add(membership.object_id)

            items_to_remove = []
            for item in self.cart:
                product_type = item['type']
                product_id = int(item['id'])
                if (product_type == COURSE_TYPE and product_id in enrolled_course_ids) or \
                        (product_type == PACKAGE_TYPE and product_id in enrolled_package_ids):
                    items_to_remove.append(item)

            if items_to_remove:
                for item in items_to_remove:
                    self.cart.remove(item)
                    product = Course.objects.get(id=item['id']) if item['type'] == COURSE_TYPE else Package.objects.get(
                        id=item['id'])
                    messages.warning(
                        self.request,
                        _(f'You\'re already enrolled in \'{product.title}\'. Removed from your cart.')
                    )
                self.save()
                items_removed = True

        course_ids = [int(item['id']) for item in self.cart if item['type'] == COURSE_TYPE]
        package_ids = [int(item['id']) for item in self.cart if item['type'] == PACKAGE_TYPE]

        courses = Course.objects.in_bulk(course_ids) if course_ids else {}
        packages = Package.objects.in_bulk(package_ids) if package_ids else {}

        self.products = {**courses, **packages}

        self.product_types = {item['id']: item['type'] for item in self.cart}

    def __iter__(self):
        """
        Iterate over the items in the cart and yield the total price of each product.
        """
        self.load_products()
        for item in self.cart:
            product_id = int(item['id'])
            product_type = self.product_types.get(item['id'])

            product = self.products.get(product_id)

            if product:
                yield {
                    'product_obj': product,
                    'item_total_price': product.discounted_price(),
                    'type': product_type,
                    'is_enrolled': False,
                }
            else:
                yield {
                    'product_obj': None,
                    'item_total_price': 0,
                    'type': product_type,
                    'is_enrolled': True,
                }

    def __len__(self):
        """Return the number of items in the cart."""
        return len(self.cart)

    def clear(self):
        """Clear the cart."""
        del self.session[self.CART_SESSION_ID]
        self.save()

    def clear_after_payment(self):
        """Clear the cart."""
        del self.session[self.CART_SESSION_ID]

        if self.CART_COUPON_CODE_ID in self.session:
            del self.session[self.CART_COUPON_CODE_ID]

        if self.CART_COUPON_DISCOUNT in self.session:
            del self.session[self.CART_COUPON_DISCOUNT]

        self.save()

    def get_total_price(self):
        """
        Calculate the total price of all products in the cart, including the coupon discount.
        Returns a tuple of (total_price, total_discounted_price).
        """
        self.load_products()
        total_price = sum(product.price for product in self.products.values())
        total_discounted_price = sum(product.discounted_price() for product in self.products.values())

        final_price = max(total_discounted_price - self.coupon_discount, 0)
        return total_price, final_price

    def apply_coupon(self, code):
        try:
            coupon = Coupon.objects.get(code=code, status=True)
            today = timezone.now().date()
            if not (coupon.date_valid_from <= today <= coupon.date_valid_to):
                raise ValueError(_('Coupon is expired or not yet valid.'))

            total_usage = CouponUsage.objects.filter(coupon=coupon).count()
            if total_usage >= coupon.max_usage_total:
                raise ValueError(_('Coupon usage limit exceeded.'))

            user = self.request.user
            if user.is_authenticated:
                user_usage = CouponUsage.objects.filter(coupon=coupon, user=user).count()
                if user_usage >= coupon.max_usage_per_user:
                    raise ValueError(_('You have exceeded the maximum usage limit for this coupon.'))

            self.coupon_code = code
            self.coupon_discount = coupon.discount_amount
            self.session['coupon_code'] = code
            self.session['coupon_discount'] = coupon.discount_amount

            self.save()

        except Coupon.DoesNotExist:
            raise ValueError(_('Invalid coupon code.'))
        except ValueError as e:
            raise ValueError(e)

    def remove_coupon(self):
        self.coupon_code = None
        self.coupon_discount = 0
        if 'coupon_code' in self.session:
            del self.session['coupon_code']
        if 'coupon_discount' in self.session:
            del self.session['coupon_discount']
        self.save()

    def finalize_purchase(self):
        """
        Finalize the purchase and record coupon usage if applicable.
        """
        user = self.request.user
        if self.coupon_code:
            try:
                coupon = Coupon.objects.get(code=str(self.coupon_code))
                CouponUsage.objects.create(coupon=coupon, user=user)
            except Coupon.DoesNotExist:
                pass

        self.clear_after_payment()
