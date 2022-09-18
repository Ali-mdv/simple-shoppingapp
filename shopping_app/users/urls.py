from django.urls import path
from .views import (Profile, AddressCreateView,
                    AddressUpdateView, AddressDeleteView,
                    UserWishListView, remove_item_wishlist, add_item_wishlist, signup, activate)

app_name = 'users'
urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),

    path('addresses/', AddressCreateView.as_view(), name='address'),
    path('address/update/<int:pk>',
         AddressUpdateView.as_view(), name='address-update'),
    path('address/delete/<int:pk>',
         AddressDeleteView.as_view(), name='address-delete'),

    path('wishlist/', UserWishListView.as_view(), name='wishlist'),
    path('wishlist/add', add_item_wishlist, name='wishlist-add'),
    path('wishlist/delete/<int:pk>', remove_item_wishlist, name='wishlist-delete'),


    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
