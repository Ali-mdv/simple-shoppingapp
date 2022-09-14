from django.urls import path
from .views import add_order, detail_cart, delete_item_order, send_request, verify

app_name = 'order'
urlpatterns = [
    path('order-list/', add_order, name='add_order'),
    path('cart/', detail_cart, name='cart'),
    path('delete-item/<int:item_id>', delete_item_order, name='delete_item'),
    path('request/', send_request, name='request'),
    path('verify/<int:order_id>', verify, name='verify'),
]
