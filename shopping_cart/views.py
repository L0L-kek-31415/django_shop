import datetime
import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from shopping_cart.models import OrderItem, Order
from user.models import Profile
from main.models import Catalog


def generate_order_id():
    date_str = datetime.date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str


def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    try:
        user_profile = get_object_or_404(Profile, user=request.user)
    except Exception:
        user_profile = Profile(user=request.user)
        user_profile.save()

    product = Catalog.objects.filter(id=kwargs.get('item_id', '')).first()
    if product in user_profile.ebooks.all():
        messages.info(request, "You already own this ebook")
        return redirect('home')
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    user_order.save()
    order_item.save()

    messages.info(request, 'item added to cart')
    return redirect('home')


def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    while item_to_delete.exists():
        try:
            item_to_delete = OrderItem.objects.filter(pk=item_id)
        except Exception:
            break
        if item_to_delete.exists():
            item_to_delete[0].delete()
            messages.info(request, "Item has been deleted")
    return redirect('cart')


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request):
    # user_order = Order.objects.get_or_create(owner=request.user.profile)
    # context = user_order[0].get_cart_items()
    # if context:
    #     for object in context:

    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
    }
    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def update_transaction_records(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    order_to_purchase.is_ordered = True
    order_to_purchase.ref_code = generate_order_id()
    order_to_purchase.date_ordered = datetime.datetime.now().tzname()
    order_to_purchase.save()

    order_items = order_to_purchase.items.all()

    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    user_profile = get_object_or_404(Profile, user=request.user)

    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()

    messages.info(request, "Your items have been paid and added to your profile")
    return redirect('my_profile')


@login_required()
def process_payment(request, order_id):
    return redirect(reverse('shopping_cart:update_records',
                            kwargs={
                                'order_id': order_id
                            }))
