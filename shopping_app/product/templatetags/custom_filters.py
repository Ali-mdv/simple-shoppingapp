from django import template


register = template.Library()


@register.filter
def price(value):
    return f"{round(value/10):,} تومان"
