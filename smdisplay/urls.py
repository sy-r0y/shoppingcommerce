# URLs

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.index),
    path('smdisplay', views.index),
    path('store', views.store, name='store'),
    path('checkout', views.checkout, name='checkout'),
    path('cart', views.cart, name='cart'),
    path('store', views.store, name='store'),
    path('productdetail/<int:pk>', views.product_detail, name='productdetail'),
    path('update_item', views.updateItem, name='updateitem'),
    path('process_order', views.processOrder, name='process_order'),

] 