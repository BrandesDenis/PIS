from datetime import date

from django import template
from django.db.models import Model

from apps.core.dates import date_pretty_format


register = template.Library()


@register.filter()
def choice_field_display(value: Model, field_name: str) -> str:
    try:
        res = getattr(value, f'get_{field_name}_display')()
    except AttributeError:
        res = ''

    return res


@register.filter()
def date_format(value: date) -> str:
    return date_pretty_format(value)


@register.filter()
def none_format(value: date) -> str:
    return '' if value is None else value
