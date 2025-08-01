from django import template
from django.contrib.contenttypes.models import ContentType

from apps.courses.models import Course, Package, CourseMembership

register = template.Library()



@register.filter
def is_enrolled(product, user_memberships):
    """
    Check if a user is enrolled in a product (Course/Package).

    Args:
        product: A Course/Package instance or a dictionary with 'product_type' and 'id'.
        user_memberships: A dictionary of pre-fetched memberships for the user, keyed by (content_type_id, object_id).

    Returns:
        bool: True if the user is enrolled, False otherwise.
    """
    if not user_memberships:
        return False

    # Case 1: Product is a model instance (Course/Package)
    if hasattr(product, '_meta'):
        content_type = ContentType.objects.get_for_model(product)
        product_id = product.id

    # Case 2: Product is a dictionary (from combined queryset)
    elif isinstance(product, dict):
        product_type = product.get('product_type')
        product_id = product.get('id')
        if product_type == 1:
            content_type = ContentType.objects.get_for_model(Course)
        elif product_type == 2:
            content_type = ContentType.objects.get_for_model(Package)
        else:
            return False
    else:
        return False

    # Check if the user is enrolled using the pre-fetched memberships
    return (content_type.id, product_id) in user_memberships

# @register.filter
# def is_enrolled(product, user):
#     if not user.is_authenticated:
#         return False
#
#     # Case 1: Product is a model instance (Course/Package)
#     if hasattr(product, '_meta'):
#         content_type = ContentType.objects.get_for_model(product)
#         product_id = product.id
#
#     # Case 2: Product is a dictionary (from combined queryset)
#     elif isinstance(product, dict):
#         product_type = product.get('product_type')
#         product_id = product.get('id')
#         if product_type == 1:
#             content_type = ContentType.objects.get_for_model(Course)
#         elif product_type == 2:
#             content_type = ContentType.objects.get_for_model(Package)
#         else:
#             return False
#     else:
#         return False
#
#     return CourseMembership.objects.filter(
#         user=user,
#         content_type=content_type,
#         object_id=product_id
#     ).exists()
