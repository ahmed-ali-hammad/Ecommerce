var addCart = document.getElementsByClassName("add-to-cart");

function updateUserOrder(productId, action){

	var data = {"productid": productId, "action": action};
	fetch('/add/to/cart/',{
		method: 'POST',
    	headers: { 
    		'Content-Type': 'application/json',
    		'X-CSRFToken' : csrftoken,
    	},
		body: JSON.stringify(data)
		})

		.then(response => response.json())
		.then(data => {document.getElementById("cart-total").innerHTML = data['total_quantity']})	

};	

function addCookieItem (productId, action){
	console.log("user is not authenticated...")


	if(action == "add"){
		if(cart[productId] == undefined){
			cart[productId] = {"quantity": 1}
		}
		else{
			cart[productId]["quantity"] +=1
		}
		
	}
	else{
		cart[productId]["quantity"] -=1
		if(cart[productId]["quantity"] <= 0){
			delete cart[productId]
		}
	}

	var totalQuantity = 0

	var cartValues = Object.values(cart)

	for (var i=0; i < cartValues.length; i++){
		totalQuantity += cartValues[i]['quantity'] 
	}

	document.getElementById("cart-total").innerHTML = totalQuantity

	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

for(var i=0 ; i < addCart.length ; i++) {

	addCart[i].addEventListener("click", function(){
			var productId = this.dataset.id;
			var action = this.dataset.action;
			

			if(user == "AnonymousUser"){
				addCookieItem(productId, action)}

			else {
				updateUserOrder(productId, action)
			};
		});

}



var cartQuantity = document.getElementsByClassName("quantity");

for(var i=0 ; i < cartQuantity.length ; i++) {

	cartQuantity[i].addEventListener("click", function(i) {

  		document.location.reload(true)})
}


