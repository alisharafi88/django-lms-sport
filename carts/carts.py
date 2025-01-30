from courses.models import Course


class Cart:
    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        """
        Initialize the cart for courses
        """
        self.request = request
        self.session = request.session

        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            cart = self.session[self.CART_SESSION_ID] = []
        self.cart = cart

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
        Remove a course from the cart
        """
        course_id = str(course.id)
        if course_id in self.cart:
            self.cart.remove(course_id)
            self.save()

    def __iter__(self):
        """
        Iterate over the course IDs in the cart and yield the total price of each course.
        """
        course_ids = list(self.cart)
        courses = Course.objects.filter(id__in=course_ids)
        cart = {course_id: {} for course_id in course_ids}

        for course in courses:
            cart[str(course.id)]['course_obj'] = course

        for item in cart.values():
            item['item_total_price'] = item['course_obj'].discounted_price()
            yield item

    def __len__(self):
        """
        Return the number of items in the cart.
        """
        return len(self.cart)

    def clear(self):
        """
        Clear the cart
        """
        del self.session[self.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Calculate the total price of all courses in the cart.
        """
        course_ids = list(self.cart)
        courses = Course.objects.filter(id__in=course_ids)
        total_price = sum(course.price for course in courses)
        total_discounted_price = sum(course.discounted_price() for course in courses)
        return total_price, total_discounted_price
