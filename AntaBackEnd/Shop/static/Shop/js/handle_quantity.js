// These two functions are in the quick view modal not in the cart template

function increaseQuantity() {
    const quantityInput = document.getElementById('quantity');

    socket.send(JSON.stringify({'type':'add-to-cart',
        'item':{'id':document.getElementById('prd_id').value,'quantity':parseInt(quantityInput.value) + 1}
        }));
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (parseInt(quantityInput.value) > 1) {

        socket.send(JSON.stringify({'type':'add-to-cart',
        'item':{'id':document.getElementById('prd_id').value,'quantity':parseInt(quantityInput.value) - 1}
        }));
    }else{
        return
    }
}