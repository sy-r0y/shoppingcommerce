

// console.log('hello world')

// let's query all the buttons by the class 'update-cart' and then add an EVENT HANDLER in a loop

var updateBtns= document.getElementsByClassName('update-cart')

for (i=0; i< updateBtns.length; i++){
    
    // Add an Event Handler
    updateBtns[i].addEventListener('click', function(){
        var productId= this.dataset.product   // this.dataset.product-- here 'product' is the attribute we added at our template store.html
        var action= this.dataset.action    // action data attribute
        //console.log('ID: ', productID, " || ", '@action: ', action)
        //console.log("User: ", user)

        if(user == 'AnonymousUser'){
            
            //console.log('Anonymous User')
            // Since user is not logged in i.e anonymous user.. call the "addCookieItem" function to handle the cookie based cart
            updateCookieItem(productId, action)
        }
        else{

            //console.log('Hello there- ', user)
            //console.log('ID & Action- ', productID, action)
            //console.log('Action is- ', action)
            

            // Send the product ID of the button/element upon which the 'action' was performed
            // Send the 'action' performed(add or remove)
            // View function will receive these data.. and then make changes to the model
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){

    console.log('Function Called. User is logged in. Product ID & Action- ', productId, action)

    //console.log('hello from function', produtId, action)
    
    var url= "update_item"

    fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json',
                  'X-CSRFToken': csrftoken, 
                  
                 },
        body: JSON.stringify({'productID': productId, 'action': action}) // we can't just send the object to the backend, hence we needed to STRINGIFY the object
    })
    .then((response) => {return response.json()})
    
    .then((data) => {
        console.log('data returned: ', data)
        location.reload()
    })

    /* Whenever we are sending POST data to the backend/server in Django
       We need to send CSRF token.
       Normally we do the CSRF token within the form (like {% csrf_token %}). 
       But in JavaScript, we don't have the Form
       Create the CSRF token within the script tag in the base.html
    */
}

function updateCookieItem(productId, action){

    // Handle the cart items, additions/removal of items in the cart... in case the user is not logged in
    // i.e handle the cart operations for "Guest/Anonymous" user

    console.log("Hello Anonymouse/Guest User!!")
    //console.log('ProductID & Action- ', productId, action)

    if(action =='add'){
        console.log("Add Item", productId, action);

        if(cart[productId]== undefined){
            cart[productId]= { 'quantity' : 1 }
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        console.log("Remove Item", productId, action)
        
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <=0 ){
            delete cart[productId];
            console.log('Item Deleted From Cart')
        }
        
    }
    
    // Now set the cookie so that even if page reloads, cookie remains & user's browser can access the cookie values

    console.log("Cart- ", cart)
    
    document.cookie= 'cart=' + JSON.stringify(cart) + ';domain=;path=/'

    location.reload()  // refresh the page



}
