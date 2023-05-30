from django import template
from product.models import Product, Category


register = template.Library()


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
