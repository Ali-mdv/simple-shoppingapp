from django.urls import path
from .views import Profile ,signup ,activate

app_name = 'users'
urlpatterns = [
    path('profile/',Profile.as_view(),name='profile'),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>',activate, name='activate'),
]



