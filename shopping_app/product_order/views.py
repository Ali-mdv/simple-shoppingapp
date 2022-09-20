from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
import requests
from datetime import datetime
from decouple import config
from .forms import NewOrderFrom
from .models import Order, OrderDetail
from product.models import Product


# Create your views here.


@login_required
def add_order(request):
    new_order_form = NewOrderFrom(request.POST or None)

    if new_order_form.is_valid():
        try:
            order = Order.objects.get(owner_id=request.user.id, is_paid=False)
        except:
            order = Order.objects.create(
                owner_id=request.user.id, is_paid=False)

        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')
        product = Product.objects.get(id=product_id)

        if count < 0:
            count = 1

        order.orderdetail_set.create(
            product_id=product.id, price=product.get_total_price(), count=count)
        print(order.orderdetail_set.all())
    return redirect('product:detail', uuid=product.uuid)


@login_required
def detail_cart(request):
    try:
        order = Order.objects.get(owner_id=request.user.id, is_paid=False)
    except:
        order = Order.objects.create(owner_id=request.user.id, is_paid=False)

    details_orders = order.orderdetail_set.filter(
        order__owner=request.user, order__is_paid=False)

    context = {
        'details_orders': details_orders,
        'order': order,
    }

    return render(request, 'order/cart.html', context)


@login_required
def delete_item_order(request, item_id):
    next = request.GET.get("next")
    try:
        # order = request.user.order_set.get(orderdetail__id=item_id)
        order_detail = OrderDetail.objects.get(
            id=item_id, order__owner_id=request.user.id)

        if order_detail is not None:
            order_detail.delete()
    except:
        raise Http404('چنین محصولی در سبد خرید شما وجود ندارد.')

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def select_address(request):
    try:
        order = Order.objects.get(owner_id=request.user.id, is_paid=False)
    except:
        return redirect("order:cart")

    addresses = request.user.useraddress_set.all()

    if request.POST:
        try:
            address = addresses.get(id=request.POST.get("address"))
            order.address = address
            order.save()
            return redirect("order:checkout-order")
        except:
            return redirect("order:address-order")

    context = {
        'addresses': addresses
    }

    return render(request, 'order/select_address.html', context)


@login_required
def checkout_order(request):
    try:
        order = Order.objects.get(owner_id=request.user.id, is_paid=False)
    except:
        order = Order.objects.create(owner_id=request.user.id, is_paid=False)

    details_orders = order.orderdetail_set.filter(
        order__owner=request.user, order__is_paid=False)

    if not details_orders:
        return redirect("order:cart")

    if not order.address:
        return redirect("order:address-order")

    context = {
        'details_orders': details_orders,
        'order': order,
    }

    return render(request, 'order/checkout.html', context)


@login_required
def send_request(request):
    if request.POST:
        try:
            order = Order.objects.get(owner_id=request.user.id, is_paid=False)
        except:
            return redirect("order:cart")

        # send data to payment gateway(zarinpal)
        params = {
            "merchant_id": config("MERCHANT_ID"),
            "amount": order.total_payment(),
            "callback_url": request.build_absolute_uri(reverse("order:verify")),
            "description": "خرید کالای از فروشگاه آنلاین شهر تاب",
            # "metadata": {request.user.email, request.user.phonenumber, },
        }

        response = requests.post(
            'https://api.zarinpal.com/pg/v4/payment/request.json', params)

        if response.json()["data"]["code"] == 100:
            authority = response.json()["data"]["authority"]
            order.ref_id = authority
            order.save()
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')

        else:
            return redirect("order:checkout-order")

    return redirect("product:home")


@login_required
def verify(request):
    try:
        order = Order.objects.get(
            owner_id=request.user.id, ref_id=request.GET.get("Authority"))
    except:
        return redirect("order:cart")
    if (request.GET.get("Status") == "OK"):
        # send data to payment gateway to verify payment(zarinpal)
        params = {
            "merchant_id": config("MERCHANT_ID"),
            "amount": order.total_payment(),
            "authority": order.ref_id
        }
        response = requests.post(
            'https://api.zarinpal.com/pg/v4/payment/verify.json', params)

        try:
            if response.json()["data"]["code"] == 100:
                order.is_paid = True
                order.payment_date = datetime.now()
                order.save()
                order.change_count_sold()
        except:
            pass

    context = {
        "order": order
    }
    return render(request, "order/verify_payment.html", context)
