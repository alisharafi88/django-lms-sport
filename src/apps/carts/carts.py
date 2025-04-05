from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

from apps.courses.models import Course, Package, CourseMembership

COURSE_TYPE = 'course'
PACKAGE_TYPE = 'package'


class Cart:
    CART_SESSION_ID = 'cart'

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

    def add(self, product):
        """
        Add a product (either Course or Package) to the cart.
        """
        product_type = COURSE_TYPE if isinstance(product, Course) else PACKAGE_TYPE
        product_id = str(product.id)
        item = {'type': product_type, 'id': product_id}

        user = self.request.user
        if user.is_authenticated:
            content_type = ContentType.objects.get_for_model(product)
            if CourseMembership.objects.filter(
                    user=user,
                    content_type=content_type,
                    object_id=product.id
            ).exists():
                messages.warning(self.request, "You're already enrolled in this product.")
                return  # Skip adding to cart

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
            return  # Skip if already loaded

        user = self.request.user
        items_removed = False

        if user.is_authenticated:
            course_ct = ContentType.objects.get_for_model(Course)
            package_ct = ContentType.objects.get_for_model(Package)

            enrolled_course_ids = set(
                CourseMembership.objects.filter(
                    user=user,
                    content_type=course_ct
                ).values_list('object_id', flat=True)
            )

            enrolled_package_ids = set(
                CourseMembership.objects.filter(
                    user=user,
                    content_type=package_ct
                ).values_list('object_id', flat=True)
            )

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
                    product = Course.objects.get(id=item['id']) if item['type'] == COURSE_TYPE else Package.objects.get(id=item['id'])
                    messages.warning(
                        self.request,
                        f'You\'re already enrolled in \'{product.title}\'. Removed from your cart.'
                    )
                self.save()
                items_removed = True

        course_ids = [int(item['id']) for item in self.cart if item['type'] == COURSE_TYPE]
        package_ids = [int(item['id']) for item in self.cart if item['type'] == PACKAGE_TYPE]

        courses = Course.objects.in_bulk(course_ids) if course_ids else {}
        packages = Package.objects.in_bulk(package_ids) if package_ids else {}

        self.products = {**courses, **packages}

    def __iter__(self):
        """
        Iterate over the items in the cart and yield the total price of each product.
        """
        self.load_products()
        for item in self.cart:
            product_type, product_id = item['type'], int(item['id'])
            product = self.products.get(product_id)

            if product:
                yield {
                    'product_obj': product,
                    'item_total_price': product.discounted_price(),
                    'type': product_type,
                    'is_enrolled': False,
                }
            else:
                product = Course.objects.get(id=product_id) if product_type == COURSE_TYPE else Package.objects.get(
                    id=product_id)
                yield {
                    'product_obj': product,
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

    def get_total_price(self):
        """
        Calculate the total price of all products in the cart.
        Returns a tuple of (total_price, total_discounted_price).
        """
        self.load_products()
        total_price = sum(product.price for product in self.products.values())
        total_discounted_price = sum(product.discounted_price() for product in self.products.values())
        return total_price, total_discounted_price
