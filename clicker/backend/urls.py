from django.urls import path
from . import views

boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boost_details = views.BoostViewSet.as_view({
    'put': 'partial_update',
})


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('update_coins/', views.update_coins, name='update_coins'),
    path('core/', views.get_core, name='get_core'),
    path('', views.index, name='index'),
    path('boosts/', boosts_list, name='boosts'),
    path('boosts/<int:pk>', boost_details, name='boosts')
]


