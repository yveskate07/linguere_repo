// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Événements
    //document.querySelector('.cart-count').addEventListener('click', toggleCartModal);
    //document.getElementById('close-cart').addEventListener('click', toggleCartModal);

    // Fermer les modales en cliquant à l'extérieur
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('quick-view-modal')) {
            closeQuickView();
        }
        if (event.target === document.getElementById('cart-modal')) {
            toggleCartModal();
        }
        if (event.target === document.getElementById('payment-modal')) {
            closePaymentModal();
        }
    });

});

function toggleCartModal() {
    const cartModal = document.getElementById('cart-modal');
    if (cartModal.style.display === 'block') {
        cartModal.style.display = 'none';
    } else {
        cartModal.style.display = 'block';
    }
}

function emptyCartModal() {
    cart = [];
    total = 0;
    updateCartDisplay();
}

// Fonction pour afficher la confirmation
function showConfirmation() {
    const confirmation = document.getElementById('confirmation-message');
    confirmation.style.display = 'block';
    confirmation.style.opacity = '1';

    setTimeout(() => {
        confirmation.style.opacity = '0';
        setTimeout(() => confirmation.style.display = 'none', 300);
    }, 3000);
}

function addToCart(quantity, prd_id) {

    socket.send(JSON.stringify({'type':'add-to-cart',
        'item':{'id':prd_id,'quantity':quantity}
        }));
}

function updateCartCountDisplay(){
    const cartCountElement = document.querySelector('.cart-count');
    // Calculer les réductions selon les nouvelles règles
    const { discount, subtotal, gift } = calculateDiscounts();

    // Ajouter la section des réductions/cadeaux
    if (discount > 0 || gift) {
        const discountElement = document.createElement('div');
        discountElement.className = 'cart-discounts';

        let discountHTML = '';
        if (discount > 0) {
            discountHTML += `
                <div class="discount-item">
                    <span>Réduction (10% sur kits Arduino/Robotique)</span>
                    <span class="text-danger">-${discount.toLocaleString()} CFA</span>
                </div>
            `;
        }

        if (gift) {
            discountHTML += `
                <div class="gift-item">
                    <span><i class="fas fa-gift text-success"></i> ${gift}</span>
                </div>
            `;
        }

        discountElement.innerHTML = discountHTML;
        cartItemsContainer.appendChild(discountElement);
    }

    // Mettre à jour le total
    const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCountElement.setAttribute('data-count', itemCount);
    cartCountElement.innerHTML = `<i class="fas fa-shopping-cart"></i> <span class="d-none d-md-inline">${subtotal.toLocaleString()} CFA</span>`;

    document.getElementById('total-price').textContent = `${subtotal.toLocaleString()} CFA`;
    document.getElementById('total-amount').textContent = subtotal.toLocaleString();
}

function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cart-items');

    // Vider le conteneur
    cartItemsContainer.innerHTML = '';
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Votre panier est vide.</p>';
        document.getElementById('total-amount').textContent = '0';
        document.querySelector('.cart-count').setAttribute('data-count', 0);
        document.querySelector('.cart-count').innerHTML = `<i class="fas fa-shopping-cart"></i> <span class="d-none d-md-inline">0 CFA</span>`;
    }
    else{
    // Ajouter chaque article
    cart.forEach((item, index) => {
        if (item.quantity > 0) {
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item';
        itemElement.innerHTML = `
            <div class="cart-item-image">
                <img src="${item.image}" alt="${item.name}" loading="lazy">
            </div>
            <div class="cart-item-info">
                <h5>${item.name}</h5>
                <p>${item.price.toLocaleString()} CFA</p>
                <small>${item.category}</small>
            </div>
            <div class="cart-item-quantity">
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(-1, ${item.item_id})">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(1, ${item.item_id})">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <div class="cart-item-actions">
                <span class="cart-item-total">${(item.price * item.quantity).toLocaleString()} CFA</span>
                <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart(${index}, ${item.item_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        cartItemsContainer.appendChild(itemElement);}
    });}

    updateCartCountDisplay();
}

// Fonction pour modifier la quantité d'un article
function changeCartItemQuantity(change, item_id, item_name, html_id) {

    socket.send(JSON.stringify({'type':'change-item-quantity',
    'item':{'id':item_id, 'quantity':change, 'name':item_name, 'html_id': html_id}
    }));
 
}

// Fonction pour supprimer un article
function removeFromCart(item_id, html_id) {

    socket.send(
        JSON.stringify({
            'type':'remove-item',
            'item':item_id,
            'html_id' : html_id
    }));
}

// Initialisation AOS
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

// Données du panier (simulées)
let cartItems = [
    { id: 1, name: "Arduino Méga", price: 15000, quantity: 1, image: "Arduino mega.png", category: "Kits Arduino", stock: "in-stock" },
    { id: 2, name: "Capteur DHT11", price: 5000, quantity: 2, image: "Capteur DHT11.png", category: "Capteurs", stock: "low-stock" }
];

// Fonctions de gestion du panier
function updateQuantity(index, change) {
    const newQuantity = cartItems[index].quantity + change;
    if (newQuantity < 1) {
        removeItem(index);
    } else {
        cartItems[index].quantity = newQuantity;
        updateCartDisplay();
    }
}

function removeItem(index) {
    cartItems.splice(index, 1);
    updateCartDisplay();
}

function saveForLater(index) {
    Swal.fire({
        icon: 'info',
        title: 'Article sauvegardé',
        text: `L'article "${cartItems[index].name}" a été sauvegardé pour plus tard.`,
        confirmButtonColor: '#2178d0'
    });
}

function updateCartDisplay() {
    console.log("Panier mis à jour:", cartItems);
}

// Modal de paiement
function proceedToCheckout() {
    // cette fonction doit sauvegarder la commande ou la creer
    /*const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
    paymentModal.show();*/
    socket.send(
        JSON.stringify({
            'type':'create_new_order',
    }));

}

function selectPaymentMethod(method) {
    document.querySelectorAll('.payment-method').forEach(option => {
        option.classList.remove('selected');
    });
    document.querySelector(`.payment-method[onclick*="${method}"]`).classList.add('selected');
    document.querySelectorAll('input[name="paymentMethod"]').forEach(radio => {
        radio.checked = (radio.value === method);
    });
    document.getElementById('confirmPaymentBtn').disabled = false;

    const instructions = document.getElementById('paymentInstructions');
    if (method === 'wave') {
        instructions.innerHTML = `
            <h6><i class="fas fa-info-circle"></i> Instructions pour Wave</h6>
            <ol>
                <li>Ouvrez l'application <strong>Wave</strong>.</li>
                <li>Allez dans "Payer".</li>
                <li>Scannez le QR code ou entrez le numéro de marchand : <strong>771234567</strong>.</li>
                <li>Validez le paiement de <strong>25 000 CFA</strong>.</li>
            </ol>
            <div class="qrcode-placeholder">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=WAVE_771234567_25000" alt="QR Code Wave">
                <p class="mt-2 small text-muted">Code marchand : 771234567</p>
            </div>
        `;
    } else {
        instructions.innerHTML = `
            <h6><i class="fas fa-info-circle"></i> Instructions pour Orange Money</h6>
            <ol>
                <li>Composez <strong>*144#</strong>.</li>
                <li>Sélectionnez "Payer un marchand".</li>
                <li>Entrez le code marchand : <strong>123456</strong>.</li>
                <li>Validez le paiement de <strong>25 000 CFA</strong>.</li>
            </ol>
            <div class="qrcode-placeholder">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=ORANGE_123456_25000" alt="QR Code Orange Money">
                <p class="mt-2 small text-muted">Code marchand : 123456</p>
            </div>
        `;
    }
    instructions.style.display = 'block';
    document.getElementById('selected-payment').value = method
}

/* Confirmation de paiement
document.getElementById('confirmPaymentBtn').addEventListener('click', function() {
    const selectedMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
    const methodName = selectedMethod === 'wave' ? 'Wave Money' : 'Orange Money';

    const modal = bootstrap.Modal.getInstance(document.getElementById('paymentModal'));
    modal.hide();

    Swal.fire({
        title: 'Traitement en cours...',
        html: `Validation de votre paiement <strong>${methodName}</strong>.`,
        timer: 2000,
        timerProgressBar: true,
        didOpen: () => Swal.showLoading()
    }).then(() => {
        Swal.fire({
            icon: 'success',
            title: 'Paiement réussi!',
            text: `Votre commande a été payée avec ${methodName}.`,
            confirmButtonColor: '#2178d0'
        });
    });
});*/