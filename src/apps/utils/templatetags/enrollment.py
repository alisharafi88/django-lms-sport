from django import template
from django.contrib.contenttypes.models import ContentType

from apps.courses.models import Course, Package, CourseMembership

register = template.Library()


@register.filter
def is_enrolled(product, user):
    if not user.is_authenticated:
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

    return CourseMembership.objects.filter(
        user=user,
        content_type=content_type,
        object_id=product_id
    ).exists()
