from django import template
from django.db.models import Model


register = template.Library()


@register.filter()
def choice_field_display(value: Model, field_name: str) -> str:
    try:
        res = getattr(value, f'get_{field_name}_display')()
    except AttributeError:
        res = ''

    return res
