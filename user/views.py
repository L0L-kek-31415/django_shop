from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .froms import UserRegisterForm, UserLoginForm, UserChangeForm, EditProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext



from .models import Profile
from shopping_cart.models import Order, OrderItem


@login_required()
def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_orders': my_orders
    }
    return render(request, 'user/profile.html', context)

class EditUserView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'user/Edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class NewPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'user/change.html'
    success_url = reverse_lazy('home')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_cart = Profile.objects.get_or_create(user=request.user)
            user_cart[0].save()
            messages.success(request, 'Registration was successful')
            return redirect('home')
        else:
            messages.error(request, "Registration ERROR")
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'user/register.html', context)
