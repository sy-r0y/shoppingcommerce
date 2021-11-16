from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.http import JsonResponse 
import json
import datetime
from .utils import cookieCart, cartData

# Create your views here


def index(request):
    
    data= cartData(request)

    cartQUANTITY= data['cartQUANTITY']

    template= 'base.html'
    context= {'cartQUANTITY' : cartQUANTITY}
    return render(request, template, context)

def store(request):
    
    data= cartData(request)

    cartQUANTITY= data['cartQUANTITY']
    
    template= 'store.html'
    products= Product.objects.all()
    context= {'products':products, 'cartQUANTITY':cartQUANTITY}
    return render(request, template, context)

def checkout(request): 
    
    data= cartData(request)

    items= data['items']
    cartQUANTITY= data['cartQUANTITY']
    order= data['order']

    template= 'checkout.html'
    context={'items': items, 'order': order, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def cart(request):

    data= cartData(request)

    items= data['items']
    cartQUANTITY= data['cartQUANTITY']
    order= data['order']
        
    template= 'cart.html'
    #print('Item ID:- ', items)
    context= {'items': items, 'order': order, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def product_detail(request, pk):

    data= cartData(request)

    items= data['items']
    cartQUANTITY= data['cartQUANTITY']
    order= data['order']
    
    template='productdetail.html'
    product= Product.objects.get(id=pk)
    context={'product':product, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def updateItem(request):

    #print('update item called!!')
    data= json.loads(request.body)   # Parse the JSON object sent via the fetch() POST request (from cart.js)

    productID= data['productID']
    action= data['action']
    #print('Product ID is:- ', productID)
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


#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
    # print('Data:', request.body)

    transaction_id= datetime.datetime.now().timestamp()
    data= json.loads(request.body)  # receive the JSON POST request data
    #print('Transaction ID', transaction_id)

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        total= float(data['form']['total'])
        order.transaction_id= transaction_id

        if total == order.cartTOTAL:
            order.complete=True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer= customer,
                order= order,
                address= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode'],
            )
    else:
        print('user not logged in')

    return JsonResponse('Payment Submitted!!!', safe= False)

    
