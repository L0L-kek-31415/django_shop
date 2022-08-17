from django.conf.urls.static import static
from django.urls import path, re_path

from ShopApp import settings
from . import views

urlpatterns = [
    path('', views.main_index, name='home'),
    path('cart', views.cart, name='cart'),
    path('<int:orderby>', views.order, name='order'),
    path('create', views.AddView.as_view(), name='create'),
    path('search/', views.search, name='search')
    # re_path(r'^remove', views.cart_remove, name='cart_remove'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

