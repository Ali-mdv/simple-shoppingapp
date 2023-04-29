from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg
import random
from .models import Product, ProductGallery, Category, Comment
from product_slider.models import Slider
from product_order.forms import NewOrderFrom
from .forms import CommentModelForm
from star_ratings.models import UserRating
# from extentions.utils import mygrouper


# Create your views here.


def home_page(request):
    slider_items = Slider.objects.all()

    products = Product.objects.available().prefetch_related("category", "body_color")

    categories = Category.objects.filter(category_type="T")

    new_products = products.order_by('-created')[:7]
    # new_products_grouper = mygrouper(4, new_products)

    # If the length of the products is less than 6 dont raise an error
    random_choices = None
    if (len(new_products) >= 6):
        random_choices = random.sample(list(new_products), 6)

    top_rated_products = products.annotate(
        avg_rating=Avg("ratings__average")).order_by('-avg_rating')[:12]

    best_seller_products = products.order_by("-count_sold", "-price")[:12]
    context = {
        'slider_items': slider_items,
        # 'new_products_grouper': new_products_grouper,
        'new_products': new_products,
        'top_rated_products': top_rated_products,
        'random_choices': random_choices,
        'best_seller_products': best_seller_products,
        'categories': categories
    }

    return render(request, 'product/index.html', context)


def products_list(request, page=1):
    sorted_by = ""
    if request.GET.get("sort") in ['price', '-price', 'ratings', '-ratings']:
        sorted_by = request.GET.get("sort")

    products = Product.objects.available().prefetch_related(
        "body_color", "mattress", "category").order_by(sorted_by or '-created')

    paginator = Paginator(products, 20)  # Show 20 contacts per page.
    page_obj = paginator.get_page(page)

    context = {
        'products': page_obj,
        "sorted_by": sorted_by
    }
    return render(request, 'product/product_list.html', context)


def product_detail(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    product_gallery = ProductGallery.objects.filter(product_id=product.id)
    similar_products = Product.objects.filter(
        Q(category=product.get_model().id) and Q(category=product.get_texture().id))[0:6]

    try:  # get user comment if exist
        comment = Comment.objects.get(user=request.user, product=product)
    except:
        comment = None

    # get all commnet about this product
    comments = Comment.objects.filter(product_id=product.id)
    comment_form = CommentModelForm(
        instance=comment)  # fill user comment in form

    # create or update comment in send post request
    if (request.POST and request.user.is_authenticated):
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            try:  # if score from UserRating model(TPP) not exist raise error
                rating = UserRating.objects.for_instance_by_user(
                    product, user=request.user).score
            except:
                rating = None

            text = comment_form.cleaned_data.get("text")
            if comment:  # if user comment exist update them
                comment.text = text
                comment.rating = rating
                comment.save()
            else:
                comment = Comment.objects.create(user=request.user,
                                                 product=product, text=text, rating=rating)

        comment_form = CommentModelForm(instance=comment)

    ip_address = request.user.ip_address
    if ip_address not in product.hits.all():  # add user ip for view count for product
        product.hits.add(ip_address)

    new_order_form = NewOrderFrom(request.POST or None, initial={
        'product_id': product.id})

    context = {
        'product': product,
        'product_gallery': product_gallery,
        'similar_products': similar_products,
        'new_order_form': new_order_form,
        'comments': comments,
        "comment_form": comment_form
    }

    return render(request, 'product/product_details.html', context)


def category_product_list(request, slug, page=1):
    sorted_by = ""
    if request.GET.get("sort") in ['price', '-price', 'ratings', '-ratings']:
        sorted_by = request.GET.get("sort")

    category = get_object_or_404(Category, slug=slug, status=True)

    products = Product.objects.filter(category=category).prefetch_related(
        "body_color", "mattress", "category").order_by(sorted_by or '-created')

    suggested_products = products.annotate(
        avg_rating=Avg("ratings__average")).order_by("-avg_rating")[:6]

    paginator = Paginator(products, 15)  # Show 15 contacts per page.
    page_obj = paginator.get_page(page)

    context = {
        "category": category,
        'products': page_obj,
        "suggested_products": suggested_products,
        "sorted_by": sorted_by
    }

    return render(request, 'product/category.html', context)


def search_products(request, page=1):
    sorted_by = ""
    if request.GET.get("sort") in ['price', '-price', 'ratings', '-ratings']:
        sorted_by = request.GET.get("sort")

    search = request.GET.get('search')
    if search is not None:
        products = Product.objects.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(category__title__icontains=search)
        ).order_by(sorted_by or 'created').distinct()
        # tag = Product.objects.filter(tag__title__icontains=search)
        # print(tag)
    paginator = Paginator(products, 25)  # Show 25 contacts per page.
    page_obj = paginator.get_page(page)
    context = {
        'products': page_obj,
        'search': search,
        "sorted_by": sorted_by

    }
    return render(request, 'product/search.html', context)
