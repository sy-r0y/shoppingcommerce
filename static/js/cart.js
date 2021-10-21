

// console.log('hello world')

// let's query all the buttons by the class 'update-cart' and then add an EVENT HANDLER in a loop

var updateBtns= document.getElementsByClassName('update-cart')

for ( i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productID= this.dataset.product   // this.dataset.product-- here 'product' is the attribute we added at our template store.html
        var action= this.dataset.action
        // console.log('productID: ', productID, " || ", 'Action: ', action)

        

    })

}