from django import template

register = template.Library()


@register.filter
def in_cart(product, cart_items):
    product_id = str(product['id'])
    product_type = 'course' if product['product_type'] == 1 else 'package' if product['product_type'] == 2 else None
    return (product_id, product_type) in cart_items if product_type else False


@register.filter
def course_in_cart(course, cart_items):
    course_id = str(course.id)
    product_type = 'course'
    return (course_id, product_type) in cart_items if product_type else False


@register.filter
def package_in_cart(package, cart_items):
    package_id = str(package.id)
    product_type = 'package'
    return (package_id, product_type) in cart_items if product_type else False
