from django import template
from django.contrib.contenttypes.models import ContentType

from apps.courses.models import CourseMembership

register = template.Library()


@register.filter
def is_active(obj):
    results = obj.filter(status=True)
    return set(results)


@register.filter
def is_enrolled(course, user):
    if not user.is_authenticated:
        return False
    content_type = ContentType.objects.get_for_model(course)
    return CourseMembership.objects.filter(
        user=user,
        content_type=content_type,
        object_id=course.id
    ).exists()

