from django.conf.urls.static import static
from django.urls import path, re_path

from ShopApp import settings
from . import views
app_name = 'shopping_cart'
urlpatterns = [
    re_path(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    re_path(r'^order-summary/$', views.order_details, name="order_summary"),
    # re_path(r'^success/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    re_path(r'^delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name="delete_from_cart"),
    re_path(r'^checkout/$', views.checkout, name="checkout"),
    re_path(r'^payment/(?P<order_id>[-\w]+)/$', views.process_payment, name="process_payment"),
    re_path(r'^update-transaction/(?P<order_id>[-\w]+)/$', views.update_transaction_records, name="update_records"),

]