from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *

# Create your views here.


def index(request):
    template= 'base.html'
    context= {}
    return render(request, template, context)


def store(request):
    template= 'store.html'
    products= Product.objects.all()
    context= {'products':products}
    return render(request, template, context)

def checkout(request):
    
    # check if the user is authenticated or not
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
    else:
        items=[]
        order={'cartTOTAL':0, 'cartQUANTITY': 0}

    
    template= 'checkout.html'
    context={'items': items, 'order': order}
    return render(request, template, context)


def cart(request):

    # two scenarios- user is registered/logged-in, user is not registered/logged-in
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)  # get the order object or create the order object(if it already exists) 
                                                       # get_or_create() get the object to query it or create a new one
                                                       # get_or_create() first queries an object ..
                                                       # if get_or_create() does not find the object.. it creates it
        
        items= order.orderitem_set.all()
    else:
        items= []
        order= {'cartTOTAL':0, 'cartQUANTITY':0}
    
    template= 'cart.html'
    context= {'items': items, 'order': order}
    return render(request, template, context)


def product_detail(request, pk):
    template='productdetail.html'
    product= Product.objects.get(id=pk)
    context={'product':product}
    return render(request, template, context)
