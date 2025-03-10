from apps.courses.models import Course, Package

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
        Load all product objects into memory using `in_bulk()` to avoid redundant queries.
        """
        if self.products is None:
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
