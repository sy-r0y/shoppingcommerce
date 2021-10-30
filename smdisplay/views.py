from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.http import JsonResponse 
import json

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer= customer, complete= False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        items= []
        order= {'cartTOTAL': 0, 'cartQUANTITY': 0}
        cartQUANTITY= order['cartQUANTITY']
    
    template= 'base.html'
    context= {'cartQUANTITY':cartQUANTITY}
    return render(request, template, context)


def store(request):
    
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer= customer, complete= False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        items= []
        order= {'cartTOTAL':0, 'cartQUANTITY':0}
        cartQUANTITY= order['cartQUANTITY']
    

    template= 'store.html'
    products= Product.objects.all()
    context= {'products':products, 'cartQUANTITY':cartQUANTITY}
    return render(request, template, context)

def checkout(request):
    
    # check if the user is authenticated or not
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        items=[]
        order={'cartTOTAL':0, 'cartQUANTITY': 0}
        cartQUANTITY= order['cartQUANTITY']

    
    template= 'checkout.html'
    context={'items': items, 'order': order, 'cartQUANTITY':cartQUANTITY}
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
        cartQUANTITY= order.cartQUANTITY
    else:
        items= []
        order= {'cartTOTAL':0, 'cartQUANTITY':0}
        cartQUANTITY= order['cartQUANTITY']
    
    template= 'cart.html'
    context= {'items': items, 'order': order, 'cartQUANTITY':cartQUANTITY}
    return render(request, template, context)


def product_detail(request, pk):

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        items= []
        order= {'cartTOTAL': 0, 'cartQUANTITY': 0}
        orderQUANTITY= order['cartQUANTITY']
    
    template='productdetail.html'
    product= Product.objects.get(id=pk)
    context={'product':product, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def updateItem(request):

    data= json.loads(request.body)   # Parse the JSON object sent via the fetch() POST request (from cart.js)

    productID= data['productID']
    action= data['action']
    
    #print('Product ID: ', productID)
    #print('Action: ', action)

    customer= request.user.customer
    product= Product.objects.get(id= productID)
    
    order, created = Order.objects.get_or_create(customer= customer, complete= False)
    orderItem, created = OrderItem.objects.get_or_create(order= order, product= product)

    if action== 'add':
        orderItem.quantity= (orderItem.quantity + 1)
    elif action== 'remove':
        orderItem.quantity= (orderItem.quantity - 1)

    orderItem.save()  #  save() saves the state of this object to the model i.e save this order item in the table

    if orderItem.quantity <= 0:
        orderItem.delete()  # delete() deletes this object from the model i.e remove this order item in the table

    return JsonResponse('Item Added!!', safe= False)

    
