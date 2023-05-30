"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls', namespace='product')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('users.urls')),
    path('order/', include('product_order.urls')),
    path('contact/', include('contact.urls')),

    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]

# active django_debug_toolbar in local mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

# for serve media file
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

# for serve static file
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
