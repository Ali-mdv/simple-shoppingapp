from django.urls import path
from .views import (
                    home_page,
                    products_list,
                    product_detail,
                    filter_products,
                    pattern_product_list,
                    special_product_list,
                    popular_product_list,
                )

app_name = 'product'
urlpatterns = [
    path('',home_page,name='home'),

    path('products',products_list,name='all_products'),
    path('products/page/<int:page>',products_list,name='all_products'),

    path('detail/<slug:slug>',product_detail,name='detail'),

    path('patterns/<slug:slug>',pattern_product_list,name='products_pattern'),

    path('products/special',special_product_list,name='special_products'),

    path('search/',filter_products,name='filter_products'),

    path('products/popular',popular_product_list,name='popular_products'),


]