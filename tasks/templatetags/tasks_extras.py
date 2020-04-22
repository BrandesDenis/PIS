from django import template


register = template.Library()


@register.filter
def status_format(value):
    if value == 0:
        return "В работе"
    elif value == 1:
        return "Завершено"
    elif value == 2:
        return "Провалено"
