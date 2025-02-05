from django import template
register = template.Library()


@register.filter
def is_active(obj):
    results = obj.filter(status=True)
    return set(results)
