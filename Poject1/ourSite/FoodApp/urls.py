from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name='index'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/', views.user_list, name='user_list'),
    path('login/', views.login_view, name='login'),
    path('profile/<str:usern>/', views.user_profile, name='user_profile'),
    path('custom_password_reset/', views.custom_password_reset, name='custom_password_reset'),
    path('add_favorite/<str:username>/', views.add_favorite, name='add_favorite'),
path('leave_review/', views.leave_review, name='leave_review'),
    path('reviews/', views.review_list, name='review_list'),
]
