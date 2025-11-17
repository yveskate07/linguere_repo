// These two functions are in the quick view modal not in the cart template

function increaseQuantity() {
    const quantityInput = document.getElementById('quantity');

    quantityInput.value = parseInt(quantityInput.value) + 1;
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (parseInt(quantityInput.value) > 1) {
        quantityInput.value = parseInt(quantityInput.value) - 1;
    }else{
        return
    }
}