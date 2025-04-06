from django import template

from apps.utils.numbers.convert_numbers import PersianNumberConverter

register = template.Library()


@register.filter
def to_persian_number(value, humanize=None):
    humanize = humanize == 'humanize' if humanize is not None else False
    return PersianNumberConverter.to_persian(value, humanize=humanize)
