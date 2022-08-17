from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from ShopApp import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('shopping-cart/', include('shopping_cart.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)