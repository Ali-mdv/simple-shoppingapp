from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewOrderFrom
from .models import Order, OrderDetail
from product.models import Product

from django.http import HttpResponse
import requests
import json

from datetime import datetime
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
            product_id=product.id, price=product.price, count=count)
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
        'total': order.total_price_order,
    }

    return render(request, 'product/cart.html', context)


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


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required

# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify'


@login_required
def send_request(request, *args, **kwags):
    try:
        order = Order.objects.get(owner_id=request.user.id, is_paid=False)
    except:
        raise Http404()

    amount = order.total_price_order()
    email = request.user.email  # Optional
    mobile = '09123572710'  # Optional

    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": f'{CallbackURL}/{order.id}',
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request, *args, **kwags):
    order_id = kwags.get('order_id')

    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(
            req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order = Order.objects.get(id=order_id)
                order.is_paid = True
                order.payment_date = datetime.now()
                order.ref_if = req.json()['data']['ref_id']
                order.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
