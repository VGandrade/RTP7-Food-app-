from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.user_list, name='user_list'),
    path('login/', views.login_view, name='login'),
]