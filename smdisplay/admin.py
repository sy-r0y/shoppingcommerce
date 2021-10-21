

from django.contrib import admin
#from .models import Customer, Product, Order, OrderItem
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display= [
        'user', 'name', 'email'
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display= [
        'name', 'price', 'digital'
    ]


class OrderAdmin(admin.ModelAdmin):
    list_display= [
        'customer', 'date_ordered', 'complete', 'transaction_id'
    ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display= [
        'product', 'order', 'quantity', 'date_added'
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)


