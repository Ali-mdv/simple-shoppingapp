from django.urls import path
from .views import (add_item_order, detail_cart, delete_item_order, order_list, order_single,
                    select_address, checkout_order, send_request, verify)

app_name = 'order'
urlpatterns = [
    path('', order_list, name='order-list'),
    path('detail/<ref_id>/', order_single, name='order-single'),

    path('add-item/', add_item_order, name='add_order'),
    path('cart/', detail_cart, name='cart'),
    path('delete-item/<int:item_id>', delete_item_order, name='delete_item'),

    path('address/', select_address, name='address-order'),
    path('checkout/', checkout_order, name='checkout-order'),

    path('request/', send_request, name='request'),
    path('verify/', verify, name='verify'),
]
