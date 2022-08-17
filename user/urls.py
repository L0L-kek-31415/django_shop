from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.EditUserView.as_view(), name='edit-profile'),
    path('password/', views.NewPasswordChangeView.as_view(), name='change'),
    re_path(r'^profile/$', views.my_profile, name='my_profile')

]
