from django import template

register = template.Library()


@register.filter
def in_cart(product, cart_items):
    product_id = str(product['id'])
    product_type = 'course' if product['product_type'] == 1 else 'package' if product['product_type'] == 2 else None
    return (product_id, product_type) in cart_items if product_type else False
