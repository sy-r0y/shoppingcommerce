from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import *
from django.http import JsonResponse 
import json
import datetime

# Create your views here


def index(request):
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer= customer, complete= False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        try:
            cart= json.loads(request.COOKIES['cart'])
        except:
            cart= {}

        items= []
        order= {'cartTOTAL': 0, 'cartQUANTITY': 0, 'shipping': False}
        cartQUANTITY= order['cartQUANTITY']
        for i in cart:
            cartQUANTITY += cart[i]['quantity']
    
    template= 'base.html'
    context= {'cartQUANTITY' : cartQUANTITY}
    return render(request, template, context)

def store(request):
    
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer= customer, complete= False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        try:
            cart= json.loads(request.COOKIES['cart'])
        except:
            cart={}

        items= []
        order= {'cartTOTAL':0, 'cartQUANTITY':0, 'shipping': False}
        cartQUANTITY= order['cartQUANTITY']
        for i in cart:
            cartQUANTITY += cart[i]['quantity']
    
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
        cartTOTAL= order.cartTOTAL
    else:
        try:
            cart= json.loads(request.COOKIES['cart'])
        except:
            cart= {}
                
        items=[]
        order={'cartTOTAL':0, 'cartQUANTITY': 0, 'shipping': False}
        cartQUANTITY= order['cartQUANTITY']
        #cartTOTAL= order['cartTOTAL']
        for i in cart:
            cartQUANTITY += cart[i]['quantity']
            product= Product.objects.get(id=i)
            order['cartTOTAL'] += (product.price * cart[i]['quantity'])

            item= {
                'product':{
                    'name':product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
            }
            items.append(item)  # append the item onto the items

    template= 'checkout.html'
    context={'items': items, 'order': order, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def cart(request):

    # two scenarios- user is registered/logged-in, user is not registered/logged-in
    #cartQUANTITY=0
    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)  # get the order object or create the order object(if it already exists) 
                                                       # get_or_create() get the object to query it or create a new one
                                                       # get_or_create() first queries an object ..
                                                       # if get_or_create() does not find the object.. it creates it
        
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
        cartTOTAL= order.cartTOTAL
    else:
        # write code to handle GUEST checkout/cart via COOKIES
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {} # dummy cart incase there is no 'cart' cookie available
        
        # print('CART- ', cart)
        items= []
        order= {'cartTOTAL':0, 'cartQUANTITY':0, 'shipping': False}
        cartQUANTITY = order['cartQUANTITY']
        #cartTOTAL= order['cartTOTAL']
        for i in cart:
            cartQUANTITY += cart[i]['quantity']
            product= Product.objects.get(id=i)
            order['cartTOTAL'] += (product.price * cart[i]['quantity'])
            item= {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'itemTOTAL': order['cartTOTAL'],
            }
            items.append(item)  #  append to the existing 'items' list object
    
    template= 'cart.html'
    context= {'items': items, 'order': order, 'cartQUANTITY': cartQUANTITY}
    return render(request, template, context)

def product_detail(request, pk):

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartQUANTITY= order.cartQUANTITY
    else:
        try:
            cart= json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items= []
        order= {'cartTOTAL': 0, 'cartQUANTITY': 0, 'shipping': False}
        cartQUANTITY= order['cartQUANTITY']
        for i in cart:
            cartQUANTITY += cart[i]['quantity']
    
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


#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def processOrder(request):
    # print('Data:', request.body)

    transaction_id= datetime.datetime.now().timestamp()
    data= json.loads(request.body)
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

    
