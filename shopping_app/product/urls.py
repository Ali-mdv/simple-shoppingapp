from django.urls import path
from .views import (
    home_page,
    products_list,
    product_detail,
    search_products,
    category_product_list,
)

app_name = 'product'
urlpatterns = [
    path('', home_page, name='home'),

    path('products', products_list, name='all_products'),
    path('products/page/<int:page>', products_list, name='all_products'),

    path('detail/<slug:slug>', product_detail, name='detail'),

    path('category/<slug:slug>', category_product_list, name='category_products'),
    path('category/<slug:slug>/<int:page>',
         category_product_list, name='category_products'),

    path('search/', search_products, name='search_products'),
    path('search/<int:page>', search_products, name='search_products'),
]
