var updateBtn = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click', function(){
        var productID = this.dataset.product
        //data-product={{i.pID}} data-action="add"
        var action = this.dataset.action
        
        console.log('productID:', productID, 'action:', action)
        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            console.log('User is not authenticated')

        }else{
            //console.log('productID:', productID, 'action:', action)
            //console.log('USER:', user)
            updateUserOrder(productID, action)
        }
    })
}

function updateUserOrder(productID, action){
    console.log('(updateUserOrder) User is authenticated, sending data...')
    var url = 'http://127.0.0.1:8000/update_item/'
    //console.log(url)
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productID':productID, 'action':action })
    })

    .then((response) =>{
        return response.json()
    })


    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}