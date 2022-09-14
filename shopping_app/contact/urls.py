from django.urls import path
from .views import contact_us, about_us, faq

app_name = 'contact'
urlpatterns = [
    path('contact-us', contact_us, name='contact_us'),
    path('about-us', about_us, name='about_us'),
    path('faq', faq, name='faq'),
]
