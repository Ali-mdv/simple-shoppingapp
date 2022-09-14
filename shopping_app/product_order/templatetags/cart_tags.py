from django import template
from product_order.models import OrderDetail

register = template.Library()


@register.inclusion_tag('template_tags/detail_cart.html', takes_context=True)
def detail_cart(context):
    request = context["request"]

    try:
        order = request.user.order_set.get(is_paid=False)
    except:
        order = request.user.order_set.create(
            owner_id=request.user.id, is_paid=False)

    details_orders = order.orderdetail_set.filter(
        order__owner=request.user, order__is_paid=False)

    return {
        "request": request,
        "order": order,
        "details_orders": details_orders
    }
