
# Utillity functions go here
# utils.py would contain all the logic/code which we want to repeat across various views
# utils.py would containt the logic to handle GUEST checkout/cart feature


import json
from .models import *

def cookieCart(request):  #  function to handle guest checkout/cart via cookies 
    try:
        cart= json.loads(request.COOKIES['cart'])
    except:
        cart= {}
    
    items= []
    order = {'cartTOTAL':0, 'cartQUANTITY':0, 'shipping':False}

    cartQUANTITY= order['cartQUANTITY']
    #cartQUANTITY= 0

    for i in cart:
        #print('Value of I:- ', i)
        #print(f'value of cart[{i}]', cart[i]['quantity'])
        
        try:
            cartQUANTITY += cart[i]['quantity']
            product = Product.objects.get(id=i)
            order['cartTOTAL'] += (product.price * cart[i]['quantity'])
            item = {
                'id': product.id,
                'product':{
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'itemTOTAL': (product.price*cart[i]['quantity']),
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    
    #print('\nCart Quantity: ', cartQUANTITY)
    #print('\norder: ', order)
    #print('\nitems: ', items)
    return {'cartQUANTITY': cartQUANTITY, 'order': order, 'items': items} 

def cartData(request):

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
        # cartTOTAL= order.cartTOTAL  
    else:
        # if it's an unauthenticated user i.e guest account
        cookieData= cookieCart(request) # call cookieCart() from utils.py

        order= cookieData['order']
        items= cookieData['items']
        cartQUANTITY= cookieData['cartQUANTITY']
        #print('Order- ', order)
        #print('Quantity- ', cartQUANTITY)
        #print('Items- ', items)
    
    return{'cartQUANTITY': cartQUANTITY, 'items': items, 'order': order}

def guestCheckout(request, data):

    name= data['form']['name']
    email= data['form']['email']
    #total= data['form']['total']

    #get cookies
    cookieData= cookieCart(request) # retrieve all the order items & corresponding data from the cart
    cartQUANTITY= cookieData['cartQUANTITY']
        
    items= cookieData['items']

    # Create customer & order
    # even if user accout does not exist, we still want to create the customer & order & orderitem
    # will use E-MAIL for that guest user acount so that it can be accessed later on by that user
        
    customer, created= Customer.objects.get_or_create(email= email) 
    customer.name= name  # set the customer name value 
    customer.save() # save the customer field in the DB

    # now save the order field
    order = Order.objects.create(customer= customer, complete= False)

    # Loop through all the items & attach them to the order
    for item in items:
        product= Product.objects.get(id=item['id'])

        orderItem= OrderItem.objects.create(
                    product= product,
                    order= order,
                    quantity= item['quantity'],
                    )
    return order, customer    
