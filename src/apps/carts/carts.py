from apps.courses.models import Course


class Cart:
    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        """
        Initialize the cart for courses.
        """
        self.request = request
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            cart = self.session[self.CART_SESSION_ID] = []
        self.cart = cart
        self.courses = None  # Cache for course objects

    def add(self, course):
        """
        Add a course to the cart.
        """
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart.append(course_id)
            self.save()

    def save(self):
        """
        Save the cart in the session.
        """
        self.session.modified = True

    def remove(self, course):
        """
        Remove a course from the cart.
        """
        course_id = str(course.id)
        if course_id in self.cart:
            self.cart.remove(course_id)
            self.save()

    def load_courses(self):
        """
        Load all course objects into memory using `in_bulk()` to avoid redundant queries.
        """
        if self.courses is None:
            course_ids = [int(course_id) for course_id in self.cart]
            if course_ids:
                self.courses = Course.objects.in_bulk(course_ids)
            else:
                self.courses = {}

    def __iter__(self):
        """
        Iterate over the course IDs in the cart and yield the total price of each course.
        """
        self.load_courses()
        for course_id in self.cart:
            course = self.courses.get(int(course_id))
            if course:
                yield {
                    'course_obj': course,
                    'item_total_price': course.discounted_price(),
                }

    def __len__(self):
        """
        Return the number of items in the cart.
        """
        return len(self.cart)

    def clear(self):
        """
        Clear the cart.
        """
        del self.session[self.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calculate the total price of all courses in the cart.
        """
        self.load_courses()
        total_price = sum(course.price for course in self.courses.values())
        total_discounted_price = sum(
            course.discounted_price() for course in self.courses.values()
        )
        return total_price, total_discounted_price
