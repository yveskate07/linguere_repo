// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Événements
    document.querySelector('.cart-count').addEventListener('click', toggleCartModal);
    document.getElementById('close-cart').addEventListener('click', toggleCartModal);

    cart = document.getElementById('cart-modal').dataset.cart ? JSON.parse(document.getElementById('cart-modal').dataset.cart) : cart;
    total = document.getElementById('cart-modal').dataset.totalPrice ? parseFloat(document.getElementById('cart-modal').dataset.totalPrice) : total;

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

function addToCart(name, price, category, image, quantity, prd_id) {
    // Vérifier si le produit est déjà dans le panier
    const existingItem = cart.find(item => item.id === prd_id);

    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: prd_id,
            name: name,
            price: price,
            category: category,
            image: image,
            quantity: quantity,
            item_id: 'null'
        });
    }

    socket.send(JSON.stringify({'type':'add-to-cart',
        'item':{'id':prd_id,'quantity':quantity}
    }));

    // Mettre à jour le total
    total += price * quantity;

    // Afficher la confirmation
    //showConfirmation();
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
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(${index}, -1, ${item.item_id})">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="quantity-value">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="changeCartItemQuantity(${index}, 1, ${item.item_id})">
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
function changeCartItemQuantity(index, change, item_id) {
    const newQuantity = cart[index].quantity + change;

    if (newQuantity < 1) {
        removeFromCart(index, item_id);
    } else {
        total += cart[index].price * change;
        cart[index].quantity = newQuantity;
    }

    socket.send(JSON.stringify({'type':'change-item-quantity',
        'item':{'id':item_id, 'quantity':newQuantity}
    })); 
}

// Fonction pour supprimer un article
function removeFromCart(index, item_id) {
    const item = cart[index];
    total -= item.price * item.quantity;
    cart.splice(index, 1);

    socket.send(
        JSON.stringify({
            'type':'remove-item',
            'item':item_id
    }));
}