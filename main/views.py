from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Catalog
from .forms import CatalogForm
from shopping_cart.models import Order, OrderItem
from user.models import Profile


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        result = Catalog.objects.filter(title__contains=searched).order_by('price')
        return render(request, 'main/index.html', {"searched": searched, 'object_list': result, 'order': order})
    else:
        return render(request, 'main/index.html')


class AddView(CreateView):
    model = Catalog
    form_class = CatalogForm
    template_name = 'main/create.html'
    success_url = reverse_lazy('home')


def main_index(request):
    return redirect("order", '3')


def order(request, orderby):
    if orderby == 1:
        orderby = 'price'
    elif orderby == 2:
        orderby = '-id'
    else:
        orderby = 'id'
    try:
        searched = request.POST['searched']
        object_list = Catalog.objects.filter(title__contains=searched)
    except:
        object_list = Catalog.objects.all()
    if not request.user.is_authenticated:
        context = {
            'title': "Main page",
            'user': request.user,
            'object_list': object_list.order_by(orderby),
            'own': [],
            "current_order_products": []
        }
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        filtered_orders = Order.objects.filter(owner=user_profile, is_ordered=False)

        current_order_products = []
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            try:
                current_order_products = Order.objects.filter(owner=user_profile, is_ordered=False).first()
            except Exception:
                current_order_products = Order.objects.create(owner=request.user.profile)[0]
            current_order_products = current_order_products.get_cart_id_items()
        for i in user_profile.ebooks.all():
            print(i.id)
        print(request.user.profile.get_ebooks_id())
        for i in object_list.all():
            print(i.id)
        context = {
            'title': "Main page",
            'user': request.user,
            'object_list': object_list.order_by(orderby),
            'own': request.user.profile.get_ebooks_id(),
            "current_order_products": current_order_products,
        }

    return render(request, 'main/index.html', context)




def byid(request):
    filtered_orders = False
    object_list = Catalog.objects.order_by('-id')
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if not filtered_orders is False:
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
    context = {
        'title': "Main page",
        'user': request.user,
        'object_list': object_list,
        "current_order_products": current_order_products
    }
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')


@login_required()
def cart(request):
    user_profile = Profile.objects.filter(user=request.user).first()
    filtered_orders = Order.objects.filter(owner=user_profile, is_ordered=False)

    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        try:
            current_order_products = Order.objects.filter(owner=user_profile, is_ordered=False).first()
        except Exception:
            current_order_products = Order.objects.create(owner=request.user.profile)[0]
        current_order_products = current_order_products.get_cart_items()
    print(current_order_products)
    context_user = {
        "current_order_products": current_order_products,
    }
    return render(request, 'main/cart.html', context_user)

# user_order = Order.objects.filter(owner=user_profile, is_ordered=False)
#     context_user = {
#         "current_order_products": user_order,
#     }
#     return render(request, 'main/cart.html', context_user)


@login_required()
def create(request):
    error = ''
    if request.method == "POST":
        form = CatalogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            error = "Error"

    form = CatalogForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)
