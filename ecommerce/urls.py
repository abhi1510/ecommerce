from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from .views import (
    home_page,
    about_page,
    contact_page,
    login_page,
    register_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about', about_page, name='about'),
    path('contact', contact_page, name='contact'),
    path('login', login_page, name='login'),
    path('register', register_page, name='register'),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('cart/', include(('carts.urls', 'cart'), namespace='cart')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
