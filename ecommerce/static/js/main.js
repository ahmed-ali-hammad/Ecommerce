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

for(var i=0 ; i < addCart.length ; i++) {

	addCart[i].addEventListener("click", function(){
			var productId = this.dataset.id;
			var action = this.dataset.action;
			

			if(user == "AnonymousUser"){
				console.log('user is not authenticated')}
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
