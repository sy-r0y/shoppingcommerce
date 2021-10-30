

// console.log('hello world')

// let's query all the buttons by the class 'update-cart' and then add an EVENT HANDLER in a loop

var updateBtns= document.getElementsByClassName('update-cart')

for (i=0; i< updateBtns.length; i++){
    
    // Add an Event Handler
    updateBtns[i].addEventListener('click', function(){
        var productID= this.dataset.product   // this.dataset.product-- here 'product' is the attribute we added at our template store.html
        var action= this.dataset.action    // action data attribute
        //console.log('ID: ', productID, " || ", '@action: ', action)
        //console.log("User: ", user)

        if(user=='AnonymousUser'){
            console.log('Anonymous User')
        }else{

            //console.log('Hello there- ', user)
            //console.log('ID & Action- ', productID, action)
            //console.log('Action is- ', action)
            

            // Send the product ID of the button/element upon which the 'action' was performed
            // Send the 'action' performed(add or remove)
            // View function will receive these data.. and then make changes to the model
            updateUserOrder(productID, action)
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
}

    /* Whenever we are sending POST data to the backend/server in Django
       We need to send CSRF token.
       Normally we do the CSRF token within the form (like {% csrf_token %}). 
       But in JavaScript, we don't have the Form
       Create the CSRF token within the script tag in the base.html
    */