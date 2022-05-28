from django.shortcuts import render, get_object_or_404
from .models import Product, Pattern, ProductGallery
from django.core.paginator import Paginator
from django.db.models import Q
from product_slider.models import Slider
from extentions.utils import mygrouper
from product_order.forms import NewOrderFrom
import random

# Create your views here.


def home_page(request):
    slider_items = Slider.objects.all()

    products = Product.objects.available().select_related(
        "pattern", "body_color", "texture")

    new_products = products.order_by('-created')
    new_products_grouper = mygrouper(4, new_products)
    random_choices = random.sample(list(new_products), 3)

    special_products = Product.objects.filter(
        is_special=True, status=True).order_by('-created')[:3]
    popular_products = products.order_by('-hits')[:3]
    context = {
        'slider_items': slider_items,
        'new_products_grouper': new_products_grouper,
        'special_products': special_products,
        'random_choices': random_choices,
        'popular_products': popular_products,
    }

    return render(request, 'product/index.html', context)


def products_list(request, page=1):
    products = Product.objects.available().select_related(
        "pattern", "body_color", "texture")

    paginator = Paginator(products, 4)  # Show 4 contacts per page.
    # page_number = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'products': page_obj
    }
    return render(request, 'product/products.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    similar_products = Product.objects.filter(pattern_id=product.pattern.id)

    ip_address = request.user.ip_address
    if ip_address not in product.hits.all():
        product.hits.add(ip_address)

    new_order_form = NewOrderFrom(request.POST or None, initial={
                                  'product_id': product.id})

    context = {
        'product': product,
        'product_gallery': product_gallery,
        'similar_products': similar_products,
        'new_order_form': new_order_form,
    }

    return render(request, 'product/product_details.html', context)


def pattern_list(request):
    patterns = Pattern.objects.all()

    context = {
        'patterns': patterns,
    }

    return render(request, 'product/pattern.html', context)


def pattern_product_list(request, slug):
    pattern = Pattern.objects.get(slug=slug)

    products = Product.objects.filter(pattern=pattern).select_related(
        "pattern", "body_color", "texture")

    context = {
        'products': products,
    }

    return render(request, 'product/products.html', context)


def special_product_list(request):
    products = Product.objects.filter(is_special=True)

    context = {
        'products': products,
    }

    return render(request, 'product/products.html', context)


def filter_products(request):
    search = request.GET.get('q')

    if search is not None:
        products = Product.objects.filter(Q(title__icontains=search) | Q(
            description__icontains=search) | Q(tag__title__icontains=search), status=True)
        # tag = Product.objects.filter(tag__title__icontains=search)
        # print(tag)

    context = {
        'products': products
    }

    return render(request, 'product/search_list.html', context)


# partial view
def sidebar_pattern(request):
    patterns = Pattern.objects.all()

    context = {
        'patterns': patterns,
    }

    return render(request, 'product/sidebar.html', context)


def Popularـproducts(request):
    products = Product.objects.available().order_by('hits')


def popular_product_list(request):
    popular_products = Product.objects.available().order_by('-hits')

    context = {
        'products': popular_products,
    }

    return render(request, 'product/search_list.html', context)
