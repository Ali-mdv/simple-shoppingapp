from django import template
from product.models import Product, Category


register = template.Library()


@register.inclusion_tag('template_tags/category_aside.html')
def category_aside():
    try:
        relax_swing = Category.objects.get(slug="relax_swing")
        children_relax_swing = relax_swing.children.all()
    except:
        children_relax_swing = Category.objects.none()
    return {
        "categories": children_relax_swing
    }


@register.inclusion_tag('template_tags/category_header.html')
def category_header():
    return {
        "categories": Category.objects.filter(is_parent=True)
    }


@register.inclusion_tag('template_tags/side_block_products.html')
def special_products_sidebar(number):
    return {
        "products": Product.objects.filter(is_special=True).order_by("-discount", "-price")[:number]
    }


@register.inclusion_tag('template_tags/side_block_products.html')
def best_seller_products_sidebar(number):
    return {
        "products": Product.objects.available().order_by("-count_sold", "-price")[:number]
    }


@register.inclusion_tag('template_tags/side_block_products.html')
def most_visited_products_sidebar(number):
    return {
        "products": Product.objects.available().order_by('-hits')[:number]
    }
