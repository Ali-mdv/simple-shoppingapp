from django import template


register = template.Library()


@register.filter
def price(value):
    return f"{round(value/10):,} تومان"


@register.filter
def phone(value):
    return f"0{value.national_number}" if value else value
